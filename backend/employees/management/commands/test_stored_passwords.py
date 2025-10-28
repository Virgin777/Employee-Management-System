from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

Employee = get_user_model()

class Command(BaseCommand):
    help = 'Show current employee passwords and allow testing with stored passwords'

    def add_arguments(self, parser):
        parser.add_argument('--test-password', type=str, help='Test this password against all employees')

    def handle(self, *args, **options):
        self.stdout.write("Current employees in database:")
        self.stdout.write("=" * 50)
        
        employees = Employee.objects.all()
        
        if options['test_password']:
            test_pwd = options['test_password']
            self.stdout.write(f"Testing password '{test_pwd}' against all employees:")
            
            for employee in employees:
                if employee.check_password(test_pwd):
                    self.stdout.write(self.style.SUCCESS(f"✓ Password '{test_pwd}' works for {employee.employee_id} ({employee.email})"))
                else:
                    self.stdout.write(f"✗ Password '{test_pwd}' does NOT work for {employee.employee_id} ({employee.email})")
        else:
            for employee in employees:
                self.stdout.write(f"Employee ID: '{employee.employee_id}'")
                self.stdout.write(f"Email: '{employee.email}'")
                self.stdout.write(f"Name: {employee.first_name} {employee.last_name}")
                self.stdout.write(f"Active: {employee.is_active}")
                self.stdout.write(f"Has password: {bool(employee.password)}")
                self.stdout.write(f"Password hash: {employee.password[:50]}...")
                self.stdout.write("-" * 30)
            
            self.stdout.write(f"\nTotal employees: {employees.count()}")
            self.stdout.write("\nTo test a password, run:")
            self.stdout.write("python manage.py test_stored_passwords --test-password YOUR_PASSWORD")
