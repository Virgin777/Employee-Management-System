from django.core.management.base import BaseCommand
from employees.models import Employee
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group, Permission
from datetime import date


class Command(BaseCommand):
    help = 'Create sample employees and tokens for testing'

    def handle(self, *args, **options):
        # Create HR group
        hr_group, created = Group.objects.get_or_create(name='HR')
        employee_group, created = Group.objects.get_or_create(name='Employee')
        
        # Create sample employees
        employees_data = [
            {
                'email': 'john.doe@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'employee_id': 'EMP0002',
                'department': 'IT',
                'designation': 'Senior Developer',
                'date_of_joining': date(2023, 1, 15),
                'salary': 75000,
                'phone': '1234567890',
                'is_hr': False,
                'password': 'employee123'
            },
            {
                'email': 'jane.smith@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'employee_id': 'EMP0003',
                'department': 'Finance',
                'designation': 'Accountant',
                'date_of_joining': date(2023, 3, 10),
                'salary': 60000,
                'phone': '1234567891',
                'is_hr': False,
                'password': 'employee123'
            },
            {
                'email': 'mike.wilson@example.com',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'employee_id': 'EMP0004',
                'department': 'Sales',
                'designation': 'Sales Executive',
                'date_of_joining': date(2023, 5, 20),
                'salary': 55000,
                'phone': '1234567892',
                'is_hr': False,
                'password': 'employee123'
            }
        ]
        
        created_count = 0
        for emp_data in employees_data:
            if not Employee.objects.filter(email=emp_data['email']).exists():
                password = emp_data.pop('password')
                employee = Employee.objects.create_user(**emp_data)
                employee.set_password(password)
                employee.save()
                
                # Add to appropriate group
                if employee.is_hr:
                    employee.groups.add(hr_group)
                else:
                    employee.groups.add(employee_group)
                
                # Create token
                Token.objects.get_or_create(user=employee)
                created_count += 1
                
                self.stdout.write(f'Created employee: {employee.employee_id} - {employee.full_name}')
        
        # Create token for admin user if exists
        try:
            admin_user = Employee.objects.get(email='admin@example.com')
            token, created = Token.objects.get_or_create(user=admin_user)
            admin_user.groups.add(hr_group)
            if created:
                self.stdout.write(f'Created token for admin: {token.key}')
            else:
                self.stdout.write(f'Admin token already exists: {token.key}')
        except Employee.DoesNotExist:
            self.stdout.write('Admin user not found')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample employees with tokens')
        )
