from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from .utils import generate_qr_code
from .models import Program, Unit, UserUnit, CartItem, User
from .forms import LoginForm, AdminRegistrationForm, UserRegistrationForm
from django.contrib import messages
import logging

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
            # Create a new User instance
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set password
            user.role = form.cleaned_data['role']  # Assign role from the form
            
            # Save the user instance
            user.save()
            
            return redirect('add_user')  # Redirect to a success page
    else:
        form = UserRegistrationForm()
    return render(request, 'add_user.html', {'form': form})


def lecturer_registration(request):
    if request.method == 'POST':
        form = LecturerRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            # Set role for the user as 'LECTURER'
            user.role = User.LECTURER
            user.save()
            # Create a new LecturerProfile instance linked to the user
            lecturer_profile = form.save(commit=False)
            lecturer_profile.user = user
            lecturer_profile.save()
            return redirect('add_staff')  # Redirect to a success page
    else:
        form = LecturerRegistrationForm()
    return render(request, 'add_staff.html', {'form': form})


def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Extract user data from the form
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Create a new User instance
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Save the user instance before using it in the student profile
            user.save()
            
            # Create a new StudentProfile instance linked to the user
            student_profile = StudentProfile(
                user=user,
                reg_no=form.cleaned_data['reg_no'],
                name=form.cleaned_data['name'],
                contact=form.cleaned_data['contact'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                gender=form.cleaned_data['gender'],
                program=form.cleaned_data['program']
            )
            student_profile.save()
            
            return redirect('add_student')  # Redirect to a success page
    else:
        form = StudentRegistrationForm()
        return render(request, 'add_student.html', {'form': form})


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


def profile(request):
    # user_profile = User.objects.get(user=request.student)
    return render(request, 'profile.html', {'profile': user_profile})


def home(request):
    return render(request, 'home.html',)


def student_dashboard(request):
    return render(request, 'student_dashboard.html')


def lecturer_dashboard(request):
    return render(request, 'lecturer_dashboard.html')


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


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
    return redirect('selected_units')


@login_required
def view_cart(request):
    try:
        cart_items = CartItem.objects.filter(user=request.user)
        logger.debug(f"Retrieved {len(cart_items)} cart items for user {request.user.username}")
        return render(request, 'selected_units.html', {'cart_items': cart_items})
    except Exception as e:
        logger.error(f"Error retrieving cart items for user {request.user.username}: {e}")
        messages.error(request, "An error occurred while retrieving your cart items.")
        return render(request, 'selected_units.html', {'cart_items': []})


@login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('register_course')


@login_required
def registered_units(request):
    _units = UserUnits.objects.filter(user=request.user)
    
    # # Initialize a list to store order summaries
    # _units = []
    
    # # Iterate over user's orders
    # for UserUnits in user_units:
    #     # Retrieve order items associated with the order
      
    return render(request, 'registered_units.html')




# @login_required
# def get_units(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             selected_year_id = request.POST.get('year')
#             selected_program = Program.objects.get(id=selected_program_id)
#             selected_year = Year.objects.get(id=selected_year_id)
#             units = Unit.objects.filter(program=selected_program, year=selected_year)
#             return render(request, 'units.html', {'units': units})
#         else:
#             return render(request, 'get_units.html', {'programs': Program.objects.all(), 'years': Year.objects.all()})
#     else:
#         return redirect('login')

# @login_required
# def register_units(request):
#     if request.method == 'POST':
#         unit_ids = request.POST.getlist('add_unit')
#         user = request.user
#         for unit_id in unit_ids:
#             unit = Unit.objects.get(id=unit_id)
#             UserUnit.objects.create(user=user, unit=unit)
#         return redirect('units')  # Redirect to a page showing registered units or any other appropriate page
#     else:
#         return redirect('units')


# @login_required
# def remove_unit(request, item_id):
#     unit = CartItems.objects.get(id=item_id)
#     unit.delete()
#     messages.success(request, 'Unit removed from cart.')
#     return redirect('units')


# @login_required
# def drop_unit(request, item_id):
#     unit = Items.objects.get(id=item_id)
#     unit.delete()
#     messages.success(request, 'Unit dropped!.')
#     return redirect('units')


def attendance(request):
    return render(request, 'attendance.html')


# def process_qr_code(request):
#     qr_code_data = request.GET.get('data')
#     # Process the scanned QR code data as needed
#     return render(request, 'attendance.html', {'qr_code_data': qr_code_data})
    

# def take_attendance(request):
#     return render(request, 'take_attendance.html')


# def add_student(request):
#     if request.method == 'POST':
#         form = StudentRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()

#     else:
#         form = StudentRegistrationForm()
#     return render(request, 'add_student.html', {'form': form})


# def add_staff(request):
#     if request.method == 'POST':
#         form = LecturerRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('add_staff')
#     else:
#         form = LecturerRegistrationForm()
#     return render(request, 'add_staff.html', {'form': form})


# def attendance_analysis(request):
#     return render(request, 'attendance_analysis.html')


# def generate_qr(request):
#     if request.method == 'POST':
#         form = QRForm(request.POST)
#         if form.is_valid():
#             date = form.cleaned_data['lecture_date']
#             unit_code = form.cleaned_data['unit_code']
#             generated_qr_filename = generate_qr_code(date, unit_code)
#             # Open the generated file and serve it as a download
#             with open(generated_qr_filename, 'rb') as f:
#                 response = FileResponse(f)
#                 response['Content-Disposition'] = f'attachment; filename="{urlquote(generated_qr_filename)}"'
#                 return response
#     else:
#         form = QRForm()
#     return render(request, 'generate_qr.html', {'form': form})