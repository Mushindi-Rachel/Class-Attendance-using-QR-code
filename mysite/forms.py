from django import forms
# from .models import Lecturer


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


G_Choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=50, required=True)
    phone_no = forms.CharField(max_length=10, required=True)
    city = forms.CharField(max_length=50, required=True)
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=G_Choices)
    course = forms.CharField(max_length=50)
    password = forms.CharField(max_length=8, required=True)

    # class Meta:
    #     model = Lecturer
    #     fields = ['name', 'email', 'phone_no', 'city', ' gender', 'course', 'password']


class RegisterStudentForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=50, required=True)
    phone_no = forms.CharField(max_length=10, required=True)
    city = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=8, required=True)

    # class Meta:
    #     model = Lecturer
    #     fields = ['username', 'email', 'phone_no', 'city', 'password']
