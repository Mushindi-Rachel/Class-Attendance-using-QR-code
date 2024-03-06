from django import forms
from .models import User, CustomAdmin


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
    
class AdminRegistrationForm(forms.Form):
    class Meta:
        model = CustomAdmin
        fields = ['name', 'email', 'department', 'staff_id']


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['role'].choices = User.ROLE_CHOICES

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email


class UnitRegistrationForm(forms.ModelForm):
    name  = "Unit Registration Form"
    # class Meta:
    #     model = units
    #     fields = ['name', 'code']  


class QRForm(forms.Form):
    lecture_date = forms.DateField(label='Date (YYYY-MM-DD)')
    unit_code = forms.CharField(label='Unit Code')
