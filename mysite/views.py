import logging
from io import BytesIO
from django.core.files import File
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Value, F
from django.http import Http404
from django.http import HttpResponse
from .utils import get_attendance_progress
import qrcode
from .models import Unit, UserUnit, CartItem, QRCode, Attendance
from .models import StudentProfile, CustomAdmin, LecturerProfile
from .forms import LoginForm, AdminRegistrationForm, UserRegistrationForm
from .forms import LecturerProfileForm, StudentProfileForm, AdminProfileForm
from .forms import QRForm

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


@login_required
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


def admin_update(request):
    if request.method == 'POST':
        form = AdminProfileForm(request.POST)
        if form.is_valid():
            # Set the user_id before saving the form
            admin_profile = form.save(commit=False)
            admin_profile.user = request.user  # Assuming user is logged in
            admin_profile.save()
            return redirect('admin_profile')
    else:
        form = AdminProfileForm()
    return render(request, 'admin_update.html', {'form': form})


def lecturer_update(request):
    if request.method == 'POST':
        form = LecturerProfileForm(request.POST)
        if form.is_valid():
            lecturer_profile = form.save(commit=False)
            lecturer_profile.user = request.user  # Assign the current user to the user_id field
            lecturer_profile.save()
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
 

def lecturer_profile(request):
    if request.user.is_authenticated:
        try:
            lecturer_profile = LecturerProfile.objects.get(user=request.user)
        except LecturerProfile.DoesNotExist:
            lecturer_profile = None
        return render(request, 'lecturer_profile.html', {'lecturer_profile': lecturer_profile})
    else:
        return render(request, 'login.html')


def admin_profile(request):
    if request.user.is_authenticated:
        try:
            admin_profile = CustomAdmin.objects.get(user=request.user)
        except CustomAdmin.DoesNotExist:
            admin_profile = None
        return render(request, 'admin_profile.html', {'admin_profile': admin_profile})
    else:
        return render(request, 'login.html')


def student_profile(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
            attendance_progress_list = get_attendance_progress(user)
            return render(request, 'student_profile.html', {'student_profile': student_profile, 'attendance_progress_list': attendance_progress_list})
        except StudentProfile.DoesNotExist:
            student_profile = None
            return render(request, 'student_profile.html', {'student_profile': student_profile})
    else:
        return render(request, 'login.html')



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
    return redirect(reverse('selected_units'))


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
    try:
        # Check if the unit exists in the user's cart and get its corresponding cart item
        cart_item = CartItem.objects.get(unit_id=unit_id, user=request.user)
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    except ObjectDoesNotExist:
        messages.error(request, 'Item does not exist in your cart.')
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

def take_attendance(request):
    return render(request, 'take_attendance.html',)


@login_required
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


@login_required
def generated_qr_code(request, qr_code_id):
    qr_code = get_object_or_404(QRCode, pk=qr_code_id)
    # Assuming qr_code.qr_code_image is the field where the image is stored
    image_data = qr_code.qr_code_image.read()
    response = HttpResponse(image_data, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename=qr_code_{qr_code.unit.code}_{qr_code.lecture_date}.png'
    return response


def attendance(request):
    return render(request, 'attendance.html',)


@login_required
def record_attendance(request):
    if request.method == 'POST':
        qr_code_data = request.POST.get('qr_code_data')
        try:
            unit_code, lecture_date = qr_code_data.split(',')
            user = request.user
            unit = Unit.objects.get(code=unit_code)

            # Fetch the units associated with the currently logged-in user
            user_units = UserUnit.objects.filter(user=user)

            # Check if the user is registered for the unit
            if user_units.filter(unit=unit).exists():
                # Record attendance
                attendance = Attendance.objects.create(user=user, unit=unit, lecture_date=lecture_date)
                messages.success(request, 'Attendance recorded successfully.')
                return redirect('record_attendance')  # Redirect to a success page
            else:
                messages.error(request, 'Error: User is not registered for the unit.')
                return redirect('failure_page')  # Redirect to a failure page if not registered for the unit
        except ValueError:
            messages.error(request, 'Error: Unable to split QR code data.')
            return render(request, 'attendance.html')  # Render a page for invalid QR code data
        except Unit.DoesNotExist:
            messages.error(request, 'Error: Unit code does not exist in the database.')
            return render(request, 'attendance.html')  # Render a page for invalid unit code
    else:
        return render(request, 'student_profile.html')


@login_required
def assigned_units(request):
    if request.user.is_authenticated and request.user.role == 'LECTURER':
        assigned_units = Unit.objects.filter(lecturer=request.user)
        return render(request, 'assigned_units.html', {'assigned_units': assigned_units})
    else:
        return render(request, 'assigned_units.html')


@login_required
def attendance_records(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    unit_attendance = Attendance.objects.filter(unit=unit)
    return render(request, 'attendance_records.html', {'unit': unit, 'unit_attendance': unit_attendance})


@login_required
def choose_year(request):
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
    return render(request, 'view_units.html', {'years': years, 'selected_year': selected_year, 'units': units})


@login_required
def attendance_analysis(request, unit_id):
    unit = Unit.objects.get(id=unit_id)
    unit_attendance = UserUnit.objects.filter(unit=unit).annotate(
        total_classes=Value(unit.total_classes),
        attended_classes=F('classes_attended')
    ).filter(attended_classes__gt=0)

    for attendance in unit_attendance:
        attendance_percentage = (attendance.attended_classes / attendance.total_classes) * 100
        attendance.attendance_percentage = attendance_percentage
        attendance.absent_percentage = 100 - attendance_percentage
        attendance.save()

    context = {
        'unit_attendance': unit_attendance,
        'unit': unit,
    }

    return render(request, 'attendance_analysis.html', context)
