from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import Token
from .models import Employee


class EmployeeAdmin(UserAdmin):
    list_display = ['employee_id', 'email', 'first_name', 'last_name', 'department', 'designation', 'is_hr', 'is_active']
    list_filter = ['department', 'designation', 'is_hr', 'is_active', 'date_of_joining']
    search_fields = ['employee_id', 'email', 'first_name', 'last_name']
    ordering = ['employee_id']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('employee_id', 'first_name', 'last_name', 'phone')}),
        ('Work info', {'fields': ('department', 'designation', 'date_of_joining', 'salary')}),
        ('Permissions', {'fields': ('is_hr', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_created')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'employee_id', 'first_name', 'last_name', 'department', 'designation', 'date_of_joining', 'salary', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['date_created', 'last_login']
    
    def save_model(self, request, obj, form, change):
        # Ensure password is properly hashed when saving through admin
        if not change:  # New object
            obj.set_password(form.cleaned_data.get('password1', ''))
        elif 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        obj.save()


# Custom Token Admin to show user details
class CustomTokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'user', 'user_email', 'user_employee_id', 'created']
    list_filter = ['created']
    search_fields = ['user__email', 'user__employee_id', 'user__first_name', 'user__last_name']
    readonly_fields = ['key', 'created']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    
    def user_employee_id(self, obj):
        return obj.user.employee_id
    user_employee_id.short_description = 'Employee ID'


# Register models
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Token, CustomTokenAdmin)

# Customize admin site headers
admin.site.site_header = "Employee Management System Admin"
admin.site.site_title = "EMS Admin Portal"
admin.site.index_title = "Welcome to Employee Management System Administration"
