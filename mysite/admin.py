from django.contrib import admin
from .models import Unit
from .models import StudentProfile
from .models import LecturerProfile
from .models import User, CustomAdmin
from .models import Department, CartItem, UserUnit, Program
# # from .models import Admin

# # Register your models here.
admin.site.register(Unit)
admin.site.register(CustomAdmin)
admin.site.register(LecturerProfile)
admin.site.register(StudentProfile)
admin.site.register(User)
admin.site.register(Department)
admin.site.register(CartItem)
admin.site.register(UserUnit)
admin.site.register(Program)


