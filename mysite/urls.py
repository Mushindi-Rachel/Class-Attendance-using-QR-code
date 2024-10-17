from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_request, name='login'),
    path('home/', views.home, name='home'),
    path('admin-registration/', views.admin_registration,
         name='admin-registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register_course/', views.choose_and_display_units,
         name='register_course'),
    path('register_course/', views.choose_and_display_units,
         name='choose_and_display_units'),
    path('selected_units/register_units/', views.register_units,
         name='register_units'),
    path('register_course/add_to_cart/', views.add_to_cart,
         name='add_to_cart'),
    path('register_course/add_to_cart/<int:unit_id>/', views.add_to_cart,
         name='add_to_cart'),
    path('selected_units/remove_from_cart/<int:unit_id>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('register_course/selected_units/', views.view_cart,
         name='selected_units'),
    path('register_course/registered_units/', views.registered_units,
         name='registered_units'),
    path('take_attendance/', views.take_attendance, name='take_attendance'),
    path('generate_qr_code/', views.generate_qr_code, name='generate_qr_code'),
    path('generated_qr_code/<int:qr_code_id>/', views.generated_qr_code,
         name='generated_qr_code'),
    path('attendance/', views.attendance, name='attendance'),
    path('record_attendance/', views.record_attendance,
         name='record_attendance'),
    path('add_user/', views.add_user, name='add_user'),
    path('admins/profile/', views.admin_profile, name='admin_profile'),
    path('lecturers/profile/', views.lecturer_profile, 
         name='lecturer_profile'),
    path('students/profile/', views.student_profile, name='student_profile'),
    path('students/profile/update/', views.student_update,
         name='student_update'),
    path('lecturers/profile/update/', views.lecturer_update,
         name='lecturer_update'),
    path('admins/profile/update/', views.admin_update,
         name='admin_update'),
    path('assigned_units/', views.assigned_units, name='assigned_units'),
    path('assigned_units/attendance_records/<int:unit_id>/',
         views.attendance_records, name='attendance_records'),
    path('assigned_units/attendance_records/<int:unit_id>/',
         views.download_attendance_records, name='download_attendance_records'),
    path('attendance_analysis/', views.choose_academic_year, name='view_units'),
    path('attendance_analysis/<int:unit_id>/',
         views.attendance_analysis, name='A_analysis'),
]
