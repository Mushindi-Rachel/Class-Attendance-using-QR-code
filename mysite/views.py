from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, RegisterStudentForm
from .models import User


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
    user_profile = User.objects.get(user=request.student)
    return render(request, 'profile.html', {'profile': user_profile})


def home(request):
    return render(request, 'home.html',)


def register_course(request):
    return render(request, 'register_course.html')


def attendance(request):
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
