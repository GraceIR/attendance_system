from django.contrib import admin
from .models import Worker, Attendance

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('worker', 'date', 'check_in_time', 'signature', 'is_late')
    list_filter = ('date', 'worker')
