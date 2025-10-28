from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

Employee = get_user_model()

class Command(BaseCommand):
    help = 'Check and fix employee credentials'

    def handle(self, *args, **options):
        self.stdout.write("Checking all employees in database:")
        self.stdout.write("=" * 50)
        
        employees = Employee.objects.all()
        
        for employee in employees:
            self.stdout.write(f"Employee ID: '{employee.employee_id}'")
            self.stdout.write(f"Email: '{employee.email}'")
            self.stdout.write(f"Name: {employee.first_name} {employee.last_name}")
            self.stdout.write(f"Active: {employee.is_active}")
            self.stdout.write(f"Has password: {bool(employee.password)}")
            
            # Test common passwords
            test_passwords = ['admin123', 'emp123', 'password', '123456']
            password_found = False
            
            for pwd in test_passwords:
                if employee.check_password(pwd):
                    self.stdout.write(self.style.SUCCESS(f"✓ Current password is: {pwd}"))
                    password_found = True
                    break
            
            if not password_found:
                # Set a default password
                employee.set_password('emp123')
                employee.save()
                self.stdout.write(self.style.WARNING(f"! Set default password 'emp123' for {employee.employee_id}"))
            
            self.stdout.write("-" * 30)
        
        self.stdout.write(f"\nTotal employees: {employees.count()}")
        self.stdout.write(
            self.style.SUCCESS(
                "\nNow you can login with:\n"
                "Employee ID: EMP0001, Password: emp123\n"
                "Employee ID: EMP0002, Password: emp123\n"
                "(or whatever password was already working)"
            )
        )
