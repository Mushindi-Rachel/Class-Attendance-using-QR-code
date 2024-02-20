from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_request, name='login'),
    path('profile/', views.profile, name='profile'),
    path('home/', views.home, name='home'),
    path('login/', views.login_request, name='login'),
    path('login/', views.logout_request, name='logout'),
    path('register_course/', views.register_course, name='register_course'),
    # path('attendance/', views.attendance, name='attendance'),
    path('attendance/', views.attendance, name='scan_qr'),
    path('process_qr_code/', views.process_qr_code, name='process_qr_code'),
    path('take_attendance/', views.take_attendance, name='take_attendance'),
    path('generate_qr/', views.generate_qr, name='generate_qr'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('attendance_analysis/', views.attendance_analysis, name='A_analysis'),
]
