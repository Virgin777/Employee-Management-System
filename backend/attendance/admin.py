from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'check_in_time', 'check_out_time', 'working_hours']
    list_filter = ['status', 'date']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    date_hierarchy = 'date'
    ordering = ['-date']
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee', 'date', 'status')
        }),
        ('Time Information', {
            'fields': ('check_in_time', 'check_out_time', 'working_hours')
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
    )
