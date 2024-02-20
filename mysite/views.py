from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import FileResponse
from .utils import generate_qr_code
from .forms import LoginForm, RegisterForm, RegisterStudentForm
# from .models import User
from .forms import QRForm
import qrcode


def index(request):
    return render(request, 'mysite/base.html')


def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page
                return redirect('home')
            else:
                # Invalid login
                error_message = "Invalid username or password."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
        else:
            # Handle invalid form data
            error_message = "Invalid form submission."
            return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout_request(request):
    logout(request)
    return redirect('login')


def profile(request):
    # user_profile = User.objects.get(user=request.student)
    return render(request, 'profile.html', {'profile': user_profile})


def home(request):
    return render(request, 'home.html',)


def register_course(request):
    return render(request, 'register_course.html')


def attendance(request):
    return render(request, 'attendance.html')


def process_qr_code(request):
    qr_code_data = request.GET.get('data')
    # Process the scanned QR code data as needed
    return render(request, 'attendance.html', {'qr_code_data': qr_code_data})
    return render(request, 'attendance.html')


def take_attendance(request):
    return render(request, 'take_attendance.html')


def add_student(request):
    if request.method == 'POST':
        form = RegisterStudentForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = RegisterStudentForm()
    return render(request, 'add_student.html', {'form': form})


def add_staff(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            form.save()

    else:
        form = RegisterForm()
    return render(request, 'add_staff.html', {'form': form})


def attendance_analysis(request):
    return render(request, 'attendance_analysis.html')


def generate_qr(request):
    if request.method == 'POST':
        form = QRForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            unit_code = form.cleaned_data['unit_code']
            generated_qr_filename = generate_qr_code(date, unit_code)
            # Open the generated file and serve it as a download
            with open(generated_qr_filename, 'rb') as f:
                response = FileResponse(f)
                response['Content-Disposition'] = f'attachment; filename="{urlquote(generated_qr_filename)}"'
                return response
    else:
        form = QRForm()
    return render(request, 'generate_qr.html', {'form': form})