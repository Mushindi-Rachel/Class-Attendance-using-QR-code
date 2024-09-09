from django import forms
# from django.utils import timezone 
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomAdmin, QRCode, StudentProfile
from .models import LecturerProfile, Department


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class AdminRegistrationForm(forms.Form):
    class Meta:
        model = CustomAdmin
        fields = ['name', 'email', 'department', 'staff_id']


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=50, required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']


class AdminProfileForm(forms.ModelForm):
    staff_id = forms.CharField(max_length=30)
    name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    department = forms.ModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = CustomAdmin
        fields = ['staff_id', 'name', 'email', 'department']


class LecturerProfileForm(forms.ModelForm):
    staff_id = forms.CharField(max_length=30)
    name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    department = forms.ModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = LecturerProfile
        fields = ['staff_id', 'name', 'email', 'department']


class StudentProfileForm(forms.ModelForm):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]

    reg_no = forms.CharField(max_length=30)
    name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    contact = forms.IntegerField()
    date_of_birth = forms.DateField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    program = forms.CharField(max_length=100)

    class Meta:
        model = StudentProfile
        fields = ['reg_no', 'name', 'email', 'contact',
                  'date_of_birth', 'gender', 'program']


class QRForm(forms.Form):
    # lecture_date = forms.DateField(default="timezone.now()")
    unit_code = forms.CharField(label='Unit Code')
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)
    
    class Meta:
        model = QRCode
        fields = ['lecture_date', 'unit_code', 'latitude', 'longitude']
