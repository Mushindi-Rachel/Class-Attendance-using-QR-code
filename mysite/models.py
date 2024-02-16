from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('admin', 'Admin'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    class Meta:
        permissions = [('view_user', 'Can view user')]
        user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='%(app_label)s_%(class)s_permissions',
        related_query_name='%(app_label)s_%(class)s'
    )


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    registration_no = models.CharField(max_length=50)
    phone_number = models.BigIntegerField()
    city = models.CharField(max_length=50)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=128, choices=GENDER_CHOICES)
    course = models.CharField(max_length=50)

    def __str__(self):
        return self.user.name + "'s Profile"


class Course(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Units(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


# class Lecturer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     unit = models.ForeignKey(Units, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.name
