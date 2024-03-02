from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _('Admin')
        STUDENT = 'STUDENT', _('Student')
        TEACHER = 'TEACHER', _('Teacher')

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STUDENT)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.Role.STUDENT
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.email})"


class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer_profile')

    def __str__(self):
        return str(self.user)
