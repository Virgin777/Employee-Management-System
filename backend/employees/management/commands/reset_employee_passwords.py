from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

Employee = get_user_model()

class Command(BaseCommand):
    help = 'Reset passwords for existing employees'

    def add_arguments(self, parser):
        parser.add_argument('--employee-id', type=str, help='Employee ID to reset password for')
        parser.add_argument('--password', type=str, help='New password to set')

    def handle(self, *args, **options):
        if options['employee_id'] and options['password']:
            # Reset password for specific employee
            try:
                employee = Employee.objects.get(employee_id=options['employee_id'])
                employee.set_password(options['password'])
                employee.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Password reset for {employee.employee_id} successfully!')
                )
            except Employee.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Employee with ID {options["employee_id"]} not found!')
                )
        else:
            # Show all employees and reset default passwords
            self.stdout.write("Current employees in database:")
            employees = Employee.objects.all()
            
            for employee in employees:
                self.stdout.write(f"- ID: {employee.employee_id}, Email: {employee.email}, Name: {employee.first_name} {employee.last_name}")
                
                # Set a default password based on employee type
                if employee.is_hr:
                    default_password = 'hr123'
                else:
                    default_password = 'emp123'
                    
                employee.set_password(default_password)
                employee.save()
                
                self.stdout.write(f"  → Password set to: {default_password}")
            
            self.stdout.write(
                self.style.SUCCESS(f'\nPasswords reset for {employees.count()} employees!')
            )
            
            self.stdout.write(
                self.style.WARNING(
                    '\nNow you can login with:\n'
                    '- Employee ID + password (hr123 for HR, emp123 for others)\n'
                    '- Email + password (same passwords as above)'
                )
            )
