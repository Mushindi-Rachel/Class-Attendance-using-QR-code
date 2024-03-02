from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_request, name='login'),
    path('profile/', views.profile, name='profile'),
    path('home/', views.home, name='home'),
    path('admin-registration/', views.admin_registration, name='admin-registration'),
    path('login/', views.login_request, name='login'),
    path('login/', views.logout_request, name='logout'),
    path('home/student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('home/lecturer_dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('home/admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register_course/', views.register_course, name='register_course'),
    path('register_course/choose-year/', views.choose_year, name='choose_year'),
    path('attendance/', views.attendance, name='attendance'),
    # path('attendance/', views.attendance, name='scan_qr'),
    # path('process_qr_code/', views.process_qr_code, name='process_qr_code'),
    # path('take_attendance/', views.take_attendance, name='take_attendance'),
    # path('generate_qr/', views.generate_qr, name='generate_qr'),
    path('add_user/', views.add_user, name='add_user'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('attendance_analysis/', views.attendance_analysis, name='A_analysis'),
]
