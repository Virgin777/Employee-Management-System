from django.contrib import admin
from .models import Leave


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'status', 'applied_date']
    list_filter = ['status', 'leave_type', 'applied_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    date_hierarchy = 'applied_date'
    ordering = ['-applied_date']
    
    fieldsets = (
        ('Leave Information', {
            'fields': ('employee', 'leave_type', 'start_date', 'end_date', 'reason')
        }),
        ('Status', {
            'fields': ('status', 'approved_by', 'hr_comments')
        }),
        ('Dates', {
            'fields': ('applied_date', 'response_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['applied_date', 'response_date']
