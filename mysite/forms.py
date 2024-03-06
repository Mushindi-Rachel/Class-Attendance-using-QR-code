from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomAdmin, QRCode, StudentProfile
from .models import LecturerProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class AdminRegistrationForm(forms.Form):
    class Meta:
        model = CustomAdmin
        fields = ['name', 'email', 'department', 'staff_id']


class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError("This username is already in use.")
    #     return username

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError(
        # "This email address is already registered.")
    #     return email


class LecturerProfileForm(forms.Form):
    class Meta:
        model = LecturerProfile
        fields = ['staff_id', 'name', 'email', 'department']


class StudentProfileForm(forms.ModelForm):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]

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
    lecture_date = forms.DateField(label='Date (YYYY/MM/DD)',
                                   widget=forms.DateInput(
                                       attrs={'type': 'date'}))
    unit_code = forms.CharField(label='Unit Code')

    class Meta:
        model = QRCode
        fields = ['lecture_date', 'unit_code']
