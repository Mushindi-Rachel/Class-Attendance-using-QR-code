from django import forms
from .models import StudentProfile
from .models import LecturerProfile, User, Unit, Year


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class AdminRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        
        
class LecturerRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = LecturerProfile
        fields = ['name', 'email', 'department', 'staff_id', 'username', 'password']


class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = StudentProfile
        fields = ['reg_no', 'name', 'email', 'contact', 'date_of_birth', 'gender', 'program', 'username', 'password']


class YearSelectionForm(forms.Form):
    class meta:
        model = Year
        fields = ['Year']
                  
    
class UnitRegistrationForm(forms.ModelForm):
    name  = "Unit Registration Form"
    
    # class Meta:
    #     model = Unit
    #     fields = ['name', 'code']


class QRForm(forms.Form):
    lecture_date = forms.DateField(label='Date (YYYY-MM-DD)')
    unit_code = forms.CharField(label='Unit Code')
