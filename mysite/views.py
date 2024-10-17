import logging
import math
import datetime
from io import BytesIO
from openpyxl import Workbook
from geopy.distance import geodesic
import qrcode
from django.core.files import File
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count 
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Value, F
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import timezone
from .utils import get_attendance_progress
from .models import Unit, UserUnit, User, CartItem, QRCode, Attendance
from .models import StudentProfile, CustomAdmin, LecturerProfile, Semester
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
        return render(request,
                      'lecturer_profile.html',
                      {'lecturer_profile': lecturer_profile
                       })
    else:
        return render(request, 'login.html')


def admin_profile(request):
    if request.user.is_authenticated:
        try:
            admin_profile = CustomAdmin.objects.get(user=request.user)
        except CustomAdmin.DoesNotExist:
            admin_profile = None
        return render(request,
                      'admin_profile.html',
                      {'admin_profile': admin_profile
                       })
    else:
        return render(request, 'login.html')


def student_profile(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
            attendance_progress_list = get_attendance_progress(user)
            return render(request,
                          'student_profile.html',
                          {'student_profile': student_profile,
                           'attendance_progress_list': attendance_progress_list
                           })
        except StudentProfile.DoesNotExist:
            student_profile = None
            return render(request,
                          'student_profile.html',
                          {'student_profile': student_profile})
    else:
        return render(request, 'login.html')


@login_required
def choose_and_display_units(request):
    if request.method == 'POST':
        selected_year = request.POST.get('academic_year')
        if selected_year:
            units = Unit.objects.filter(academic_year=selected_year)
        else:
            messages.error(request, "No academic year selected.")
            units = None
    else:
        selected_year = None
        units = None

    academic_years = Unit.objects.values_list(
        'academic_year',
        flat=True).distinct().order_by('academic_year')
    return render(request, 'register_course.html', {
        'academic_years': academic_years,
        'units': units})
    
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        unit_id = request.POST.get('unit_id')
        if unit_id:
            unit = get_object_or_404(Unit, id=unit_id)
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user, unit=unit)
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
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            items = [{'id': item.id, 'name': item.unit.name} for item in cart_items]
            return JsonResponse({'cartItems': items})
        else:
            return render(request, 'register_course.html', {'cart_items': cart_items})
    except ObjectDoesNotExist:
        messages.error(request, "No items found in your cart.")
    except Http404:
        messages.error(request, "Cart items not found.")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    return render(request, 'register_course.html', {'cart_items': []})


@login_required
def remove_from_cart(request, unit_id):
    response_data = {'message': '', 'status': 'error'}
    try:
        cart_item = CartItem.objects.get(unit_id=unit_id, user=request.user)
        cart_item.delete()
        response_data['message'] = 'Item removed from cart.'
        response_data['status'] = 'success'
    except ObjectDoesNotExist:
        response_data['message'] = 'Item does not exist in your cart.'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(response_data)
    else:
        messages.success(request, response_data['message'])
        return redirect('register_course')


@login_required
def register_units(request):
    response_data = {'message': '', 'status': 'error'}
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            unit = cart_item.unit
        
            if not UserUnit.objects.filter(user=request.user, unit=unit).exists():
                # Create UserUnit object if it doesn't exist
                UserUnit.objects.create(user=request.user, unit=unit)
            else:
                response_data['message'] = "Unit already registered!"
                return JsonResponse(response_data) 
                pass

        # Clear cart items
        cart_items.delete()
        response_data['message'] = "Units registered successfully!"
        response_data['status'] = 'success'
    return JsonResponse(response_data)


@login_required
def registered_units(request):
    user_units = UserUnit.objects.filter(user=request.user)
    return render(request, 'registered_units.html', {'user_units': user_units})


def take_attendance(request):
    return render(request, 'generate_QR.html',)


ALLOWED_LOCATION = None
RADIUS_IN_METERS = 100


@login_required
def generate_qr_code(request):
    if request.method == 'POST':
        form = QRForm(request.POST)
        if form.is_valid():
            unit_code = form.cleaned_data['unit_code']

            # Check if the unit with the specified code exists
            unit = get_object_or_404(Unit, code=unit_code)
            lecture_datetime = timezone.now()
            lecture_date = lecture_datetime.date()
            qr_code_data = f"{unit_code},{lecture_date}"

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4
            )
            qr.add_data(qr_code_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Save the image to a BytesIO buffer
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)

            # Save the QR code image to the QRCode model instance
            qr_code_instance = QRCode(unit=unit, lecture_date=lecture_date)
            qr_code_instance.qr_code_image.save(
                f'qr_code_{unit_code}_{lecture_date}.png',
                File(buffer)
            )
            qr_code_instance.save()

            # Capture lecturer's location from the form
            latitude = form.cleaned_data.get('latitude')
            longitude = form.cleaned_data.get('longitude')

            if latitude and longitude:
                global ALLOWED_LOCATION
                ALLOWED_LOCATION = (float(latitude), float(longitude))
                messages.success(request, 'Allowed location set successfully.')
            else:
                messages.error(request, 'Error: Location data is missing.')

            # Redirect to a success page
            return redirect(
                'generated_qr_code', qr_code_id=qr_code_instance.pk)
    else:
        form = QRForm()
    return render(request, 'generate_QR.html', {'form': form})


@login_required
def generated_qr_code(request, qr_code_id):
    qr_code = get_object_or_404(QRCode, pk=qr_code_id)
    # qr_code.qr_code_image is the field where the image is stored
    image_data = qr_code.qr_code_image.read()
    response = HttpResponse(image_data, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename=qr_code_{qr_code.unit.code}_{qr_code.lecture_date}.png'
    return response


def attendance(request):
    return render(request, 'attendance.html',)


@login_required
def record_attendance(request):
    response_data = {'message': '', 'status': 'error'}
    
    if request.method == 'POST':
        qr_code_data = request.POST.get('qr_code_data')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if not ALLOWED_LOCATION:
            response_data['message'] = 'Error: Allowed location is not set.'
            return JsonResponse(response_data)

        if not latitude or not longitude:
            response_data['message'] = 'Error: Location data is missing.'
            return JsonResponse(response_data)

        try:
            student_location = (float(latitude), float(longitude))
            distance = geodesic(ALLOWED_LOCATION, student_location).meters
            if distance > RADIUS_IN_METERS:
                response_data['message'] = 'Error: You are not in the allowed area.'
                return JsonResponse(response_data)
            
            unit_code, lecture_date = qr_code_data.split(',')
            user = request.user
            unit = Unit.objects.get(code=unit_code)

            user_units = UserUnit.objects.filter(user=user)
            if user_units.filter(unit=unit).exists():
                Attendance.objects.create(
                    user=user,
                    unit=unit,
                    lecture_date=lecture_date
                    )
                response_data['message'] = 'Attendance recorded successfully.'
                response_data['status'] = 'success'
                return JsonResponse(response_data)
            else:
                response_data['message'] = 'Error: User is not registered for the unit.'
                return JsonResponse(response_data)
                
        except ValueError:
            response_data['message'] = 'Error: Unable to split QR code data.'
            return JsonResponse(response_data)
        except Unit.DoesNotExist:
            response_data['message'] = 'Error: Unit code does not exist in the database.'
            return JsonResponse(response_data)
    else:
        return render(request, 'student_profile.html')


@login_required
def assigned_units(request):
    if request.user.is_authenticated and request.user.role == 'LECTURER':
        assigned_units = Unit.objects.filter(lecturer=request.user)
        return render(request,
                      'assigned_units.html',
                      {'assigned_units': assigned_units})
    else:
        return render(request, 'assigned_units.html')


@login_required
def attendance_records(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    lecture_dates = list(Attendance.objects.filter(unit=unit).values_list('lecture_date', flat=True).distinct())
    most_recent_date = max(lecture_dates) if lecture_dates else None
    
    selected_date = request.GET.get('lecture_date', most_recent_date)
    
    unit_attendance = Attendance.objects.filter(unit=unit)
    if selected_date:
        unit_attendance = Attendance.objects.filter(
            unit=unit, lecture_date=selected_date)
        
    context = {
        'unit': unit,
        'unit_attendance': unit_attendance,
        'lecture_dates': lecture_dates,
        'selected_date': selected_date,
    }
    return render(request, 'attendance_records.html', context)


@login_required
def download_attendance_records(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    selected_date = request.GET.get('lecture_date-')
    return render(request, 'attendance_records.html', context)

    
@login_required
def choose_academic_year(request):
    selected_academic_year = None
    selected_semester = None
    units = None

    if request.method == 'POST':
        selected_academic_year = str(request.POST.get('academic_year'))
        selected_semester = str(request.POST.get('semester'))

        if selected_academic_year:
            units = Unit.objects.filter(
                academic_year=selected_academic_year)

            if selected_semester:
                units = units.filter(
                    userunit__semester__name=selected_semester
                                        ).distinct()
        else:
            messages.error(request, "No academic year selected.")
    else:
        units = None
    academic_years = Unit.objects.values_list(
        'academic_year', flat=True).distinct().order_by(
                                                'academic_year')
    semesters = Semester.objects.values_list(
        'name', flat=True).distinct().order_by(
                                                'name')

    return render(request, 'view_units.html', {
        'academic_years': academic_years,
        'semesters': semesters,
        'selected_academic_year': selected_academic_year,
        'selected_semester': selected_semester,
        'units': units,
    })


@login_required
def attendance_analysis(request, unit_id=None):
    unit = Unit.objects.get(id=unit_id)
    
    # Get the semester and academic year from the POST data
    selected_semester_name = request.POST.get('semester')
    selected_academic_year = request.POST.get('academic_year')
    
    # Determine date range based on selected semester
    start_date = None
    end_date = None
    
    if selected_semester_name == 'Jan-Apr':
        start_date = datetime.date(year=datetime.datetime.now(
            ).year, month=1, day=1)
        end_date = datetime.date(year=datetime.datetime.now(
            ).year, month=4, day=30)
    elif selected_semester_name == 'May-Aug':
        start_date = datetime.date(year=datetime.datetime.now(
            ).year, month=5, day=1)
        end_date = datetime.date(year=datetime.datetime.now(
            ).year, month=8, day=31)
    elif selected_semester_name == 'Sep-Dec':
        start_date = datetime.date(year=datetime.datetime.now(
            ).year, month=9, day=1)
        end_date = datetime.date(year=datetime.datetime.now(
            ).year, month=12, day=31)
    
    # Fetch attendance records
    attendance_records = Attendance.objects.filter(
        unit=unit,
        lecture_date__range=(start_date, end_date)
    ).values('user').annotate(
        attended_classes=Count('id')
    ).order_by('user')
    
    # Create an Excel workbook and worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = 'Attendance Analysis'

    # Add headers
    ws.append(['Registration No', 'Name', 'Attendance Percentage'])

    # Add attendance data
    total_classes = unit.total_classes
    for record in attendance_records:
        user = User.objects.get(id=record['user'])
        attended_classes = record['attended_classes']
        attendance_percentage = (attended_classes / total_classes) * 100
        rounded_attendance = math.ceil(attendance_percentage)
        
        ws.append([
            user.studentprofile.reg_no,
            user.studentprofile.name,
            f"{rounded_attendance}%"
        ])
        
        # Auto-size columns based on maximum length of cell contents
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width
        
    # Save workbook to a BytesIO stream
    output = BytesIO()
    wb.save(output)
    output.seek(0)
        
    # Create an HTTP response with the Excel file
    response = HttpResponse(output, content_type=
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={unit.name}_attendance.xlsx'

    return response