from django.contrib import admin
from .models import Unit, QRCode, Attendance
from .models import StudentProfile
from .models import LecturerProfile
from .models import User, CustomAdmin
from .models import Department, CartItem, UserUnit, Program, Semester


# Registering models.
admin.site.register(Unit)
admin.site.register(CustomAdmin)
admin.site.register(LecturerProfile)
admin.site.register(StudentProfile)
admin.site.register(User)
admin.site.register(Department)
admin.site.register(CartItem)
admin.site.register(Program)
admin.site.register(QRCode)
admin.site.register(Attendance)
admin.site.register(Semester)


class UserUnitAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ('user', 'unit', 'registered_on', 'semester', 'classes_attended')

    # List of fields to display in the detailed view
    fields = ('user', 'unit', 'registered_on', 'semester', 'classes_attended')

    # Make registered_on read-only if it should not be edited
    readonly_fields = ('registered_on',)


admin.site.register(UserUnit)
