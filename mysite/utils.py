from .models import UserUnit


def get_attendance_progress(user):
    attendance_progress_list = []
    user_units = UserUnit.objects.filter(user=user)

    for user_unit in user_units:
        unit = user_unit.unit
        total_classes = unit.total_classes
        classes_attended = user_unit.classes_attended
        
        if total_classes != 0:
            attendance_percentage = (classes_attended / total_classes) * 100
            absent_percentage = 100 - attendance_percentage
        else:
            attendance_percentage = 0
            absent_percentage = 0

        attendance_progress_list.append({
            'unit_code': unit.code,
            'attendance_percentage': attendance_percentage,
            'absent_percentage': absent_percentage
        })

    return attendance_progress_list
