from django.contrib import admin
from .models import Payroll


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ['employee', 'month', 'year', 'gross_salary', 'net_salary', 'generated_date']
    list_filter = ['month', 'year', 'generated_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    ordering = ['-year', '-month']
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee', 'month', 'year')
        }),
        ('Salary Components', {
            'fields': ('basic_salary', 'house_rent_allowance', 'medical_allowance', 'transport_allowance', 'bonus', 'overtime_pay')
        }),
        ('Deductions', {
            'fields': ('tax_deduction', 'provident_fund', 'insurance_deduction', 'other_deductions')
        }),
        ('Calculated Amounts', {
            'fields': ('gross_salary', 'total_deductions', 'net_salary'),
            'classes': ('collapse',)
        }),
        ('Generation Info', {
            'fields': ('generated_by', 'generated_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['gross_salary', 'total_deductions', 'net_salary', 'generated_date']
