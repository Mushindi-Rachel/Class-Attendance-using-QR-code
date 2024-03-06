from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ADMIN = 'ADMIN'
    LECTURER = 'LECTURER'
    STUDENT = 'STUDENT'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (LECTURER, 'Lecturer'),
        (STUDENT, 'Student'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    email = models.EmailField(unique=True, max_length=50)
    username = models.CharField(unique=True, max_length=20)


class CustomAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.staff_id} - {self.name} - {self.email}"


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class LecturerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    staff_id = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)

    def get_absolute_url(self):
        return "/lecturer/profile/%i/" % self.staff_id

    def __str__(self):
        return f"{self.staff_id} - {self.name} - {self.email}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contact = models.IntegerField()
    date_of_birth = models.DateField()
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    program = models.CharField(max_length=100)

    def get_absolute_url(self):
        return "/student/profile/%i/" % self.reg_no

    def __str__(self):
        return f"{self.reg_no}-{self.program}"


class Program(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Unit(models.Model):
    YEAR_CHOICES = [
        (1.1, '1.1'),
        (1.2, '1.2'),
        (2.1, '2.1'),
        (2.2, '2.2'),
        (3.1, '3.1'),
        (3.2, '3.2'),
        (4.1, '4.1'),
        (4.2, '4.2'),
    ]
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, default='INTE000')
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    year = models.FloatField(max_length=20, choices=YEAR_CHOICES, default=0.0)

    def __str__(self):
        return self.name


class UserUnit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.unit.name}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.unit.name} - Cart"
