import logging
from io import BytesIO
from django.core.files import File
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.http import HttpResponse
import qrcode
from .models import Unit, UserUnit, CartItem, User, QRCode, Attendance
from .forms import LoginForm, AdminRegistrationForm, UserRegistrationForm
from .forms import LecturerProfileForm, StudentProfileForm, QRForm

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'login.html')


def admin_registration(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'admin-registration.html', {'form': form})


def add_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']  # Set role from the form data
            user.save()
            return redirect('add_user')  # Redirect to a success page or another view
    else:
        form = UserRegistrationForm()
    return render(request, 'add_user.html', {'form': form})


def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = LoginForm()  # Create an instance of the LoginForm class
    return render(request, 'login.html', {'form': form})


def logout_request(request):
    logout(request)
    return redirect('login')


def lecturer_update(request):
    if request.method == 'POST':
        form = LecturerProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lecturer_profile')
    else:
        form = LecturerProfileForm()
    return render(request, 'lecturer_update.html', {'form': form})


def student_update(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            # Set the user_id before saving the form
            student_profile = form.save(commit=False)
            student_profile.user = request.user  # Assuming user is logged in
            student_profile.save()
            return redirect('student_profile')
    else:
        form = StudentProfileForm()
    return render(request, 'student_update.html', {'form': form})


def home(request):
    return render(request, 'home.html',)


def student_profile(request):
    if request.user.is_authenticated:
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            student_profile = None

        return render(request, 'student_profile.html', {'student_profile': student_profile})
    else:
        return render(request, 'login.html')
    

def lecturer_profile(request):
    return render(request, 'lecturer_profile.html')


def admin_profile(request):
    return render(request, 'admin_profile.html')


@login_required
def choose_and_display_units(request):
    if request.method == 'POST':
        selected_year = request.POST.get('year')
        if selected_year:
            units = Unit.objects.filter(year=selected_year)
        else:
            messages.error(request, "No year selected.")
            units = None
    else:
        selected_year = None
        units = None

    years = Unit.objects.values_list('year', flat=True).distinct()  # Retrieve distinct years
    return render(request, 'register_course.html', {'years': years, 'selected_year': selected_year, 'units': units})


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        unit_id = request.POST.get('unit_id')
        if unit_id:
            unit = get_object_or_404(Unit, id=unit_id)
            cart_item, created = CartItem.objects.get_or_create(user=request.user, unit=unit)
            if created:
                messages.success(request, "Unit added to cart successfully.")
            else:
                messages.info(request, "Unit is already in the cart.")

    # Redirect back to the same page where the user added the unit from
    return redirect(reverse('choose_and_display_units'))


@login_required
def view_cart(request):
    try:
        cart_items = CartItem.objects.filter(user=request.user)
        return render(request, 'selected_units.html', {'cart_items': cart_items})
    except ObjectDoesNotExist:
        messages.error(request, "No items found in your cart.")
    except Http404:
        messages.error(request, "Cart items not found.")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    return render(request, 'selected_units.html', {'cart_items': []})

    
@login_required
def remove_from_cart(request, unit_id):
    cart_item = CartItem.objects.get(id=unit_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('register_course')


@login_required
def register_units(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        # Register units from cart items
        for cart_item in cart_items:
            unit = cart_item.unit
            # Create UserUnit object
            UserUnit.objects.create(user=request.user, unit=unit)

        # Clear cart items
        cart_items.delete()
        messages.success(request, "Units registered successfully and cart items cleared.")
    return redirect('choose_and_display_units')


@login_required
def registered_units(request):
    user_units = UserUnit.objects.filter(user=request.user)
    return render(request, 'registered_units.html', {'user_units': user_units})
    

# @login_required
# def drop_unit(request, item_id):
#     unit = Items.objects.get(id=item_id)
#     unit.delete()
#     messages.success(request, 'Unit dropped!.')
#     return redirect('units')


def attendance(request):
    return render(request, 'attendance.html')


def take_attendance(request):
    return render(request, 'take_attendance.html')


def attendance_analysis(request):
    return render(request, 'attendance_analysis.html')


def generate_qr_code(request):
    if request.method == 'POST':
        form = QRForm(request.POST)
        if form.is_valid():
            unit_code = form.cleaned_data['unit_code']
            lecture_date = form.cleaned_data['lecture_date']
            
            # Check if the unit with the specified code exists
            unit = get_object_or_404(Unit, code=unit_code)
            
            qr_code_data = f"{unit_code},{lecture_date}"
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(qr_code_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save the image to a BytesIO buffer
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Save the QR code image to the QRCode model instance
            qr_code = QRCode(unit=unit, lecture_date=lecture_date)
            qr_code.qr_code_image.save(
                f'qr_code_{unit_code}_{lecture_date}.png',
                File(buffer))
            qr_code.save()
            
            # Redirect to a success page
            return redirect('generated_qr_code', qr_code_id=qr_code.pk)
    else:
        form = QRForm()
    return render(request, 'take_attendance.html', {'form': form})


def generated_qr_code(request, qr_code_id):
    qr_code = get_object_or_404(QRCode, pk=qr_code_id)
    # Assuming qr_code.qr_code_image is the field where the image is stored
    image_data = qr_code.qr_code_image.read()
    response = HttpResponse(image_data, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename=qr_code_{qr_code.unit.code}_{qr_code.lecture_date}.png'
    return response


def scan_qr_code(request, unit_code, lecture_date):
    # Authenticate the student (You can implement your authentication logic here)
    student = request.user  # Assuming you have a UserProfile linked to the User model

    # Check if the student is registered for the unit
    if student.units.filter(code=unit_code).exists():
        # Create attendance record
        attendance = Attendance(
            student=student,
            unit_code=unit_code,
            lecture_date=lecture_date, 
            status='present'
            )
        attendance.save()
        message = 'Attendance recorded successfully.'
    else:
        message = 'You are not registered for this unit.'

    return render(request, 'attendance_feedback.html', {'message': message})


def record_attendance(request):
    if request.method == 'POST':
        qr_code_data = request.POST.get('qr_code_data')
        print("Scanned QR code data:", qr_code_data)  # Print QR code data for debugging

        if qr_code_data:
            try:
                unit_code, lecture_date = qr_code_data.split(',')
                print("Unit Code:", unit_code)
                print("Lecture Date:", lecture_date)

                # Check if the unit code exists in the database
                try:
                    unit = Unit.objects.get(code=unit_code)
                except Unit.DoesNotExist:
                    print("Error: Unit code does not exist")
                    messages.error(request, "Error: Unit code does not exist")
                    return redirect('attendance_feedback')

                # Record attendance
                user = request.user
                Attendance.objects.create(user=user, unit=unit, lecture_date=lecture_date)
                print("Attendance recorded successfully")
                messages.success(request, "Attendance recorded successfully")
                return redirect('success_page')

            except ValueError:
                # Handle case where splitting fails
                print("Error: Unable to split QR code data")
                messages.error(request, "Error: Unable to split QR code data")
                return redirect('attendance_feedback')

        else:
            # Handle case where QR code data is empty
            print("Error: QR code data is empty")
            messages.error(request, "Error: QR code data is empty")
            return redirect('attendance_feedback')

    else:
        # Handle GET request or other methods
        return render(request, 'attendance_feedback.html')


def assigned_units(request):
    return render(request, 'assigned_units.html')
