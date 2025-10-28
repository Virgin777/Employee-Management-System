from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date

Employee = get_user_model()

class Command(BaseCommand):
    help = 'Create sample employees for testing'

    def handle(self, *args, **options):
        # Create a simple test employee first
        test_employee, created = Employee.objects.get_or_create(
            employee_id='TEST001',
            defaults={
                'email': 'test@company.com',
                'first_name': 'Test',
                'last_name': 'User',
                'phone': '1234567890',
                'date_of_joining': date(2023, 1, 1),
                'department': 'IT',
                'designation': 'Developer',
                'salary': 50000.00,
                'is_hr': False,
                'is_active': True,
            }
        )
        if created:
            test_employee.set_password('test123')
            test_employee.save()
            self.stdout.write(f'Created Test Employee: {test_employee.email} (ID: {test_employee.employee_id})')
        
        # Create an admin user
        admin_employee, created = Employee.objects.get_or_create(
            employee_id='ADMIN001',
            defaults={
                'email': 'admin@company.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'phone': '1234567891',
                'date_of_joining': date(2023, 1, 1),
                'department': 'HR',
                'designation': 'Manager',
                'salary': 75000.00,
                'is_hr': True,
                'is_staff': True,
                'is_active': True,
            }
        )
        if created:
            admin_employee.set_password('admin123')
            admin_employee.save()
            self.stdout.write(f'Created Admin: {admin_employee.email} (ID: {admin_employee.employee_id})')

        # Create regular employees from different departments
        employees_data = [
            {
                'employee_id': 'EMP001',
                'email': 'john.doe@company.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'department': 'IT',
                'designation': 'Developer',
                'salary': 80000.00,
            },
            {
                'employee_id': 'EMP002',
                'email': 'jane.smith@company.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'department': 'IT',
                'designation': 'Senior Developer',
                'salary': 95000.00,
            },
        ]

        for emp_data in employees_data:
            employee, created = Employee.objects.get_or_create(
                employee_id=emp_data['employee_id'],
                defaults={
                    'email': emp_data['email'],
                    'first_name': emp_data['first_name'],
                    'last_name': emp_data['last_name'],
                    'phone': '1234567892',
                    'date_of_joining': date(2022, 6, 1),
                    'department': emp_data['department'],
                    'designation': emp_data['designation'],
                    'salary': emp_data['salary'],
                    'is_hr': False,
                    'is_active': True,
                }
            )
            if created:
                employee.set_password('emp123')  # Default password for all employees
                employee.save()
                self.stdout.write(f'Created Employee: {employee.first_name} {employee.last_name} (ID: {employee.employee_id}, Email: {employee.email})')

        self.stdout.write(
            self.style.SUCCESS(
                '\nSample employees created successfully!\n'
                'Test login credentials:\n'
                '  - test@company.com or TEST001 (password: test123)\n'
                '  - admin@company.com or ADMIN001 (password: admin123)\n'
                '  - john.doe@company.com or EMP001 (password: emp123)\n'
                '  - jane.smith@company.com or EMP002 (password: emp123)\n'
            )
        )
