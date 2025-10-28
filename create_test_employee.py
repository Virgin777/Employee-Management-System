import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append('c:/Users/virgi/OneDrive/Desktop/Employee Management Systemsss/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')
django.setup()

from employees.models import Employee
from datetime import date

# Create a test employee with correct field names
try:
    # Delete existing employee if exists
    Employee.objects.filter(employee_id='TEST001').delete()
    
    test_employee = Employee.objects.create(
        employee_id='TEST001',
        email='test@company.com',
        first_name='Test',
        last_name='User',
        phone='1234567890',
        department='IT',
        designation='Developer',
        date_of_joining=date(2023, 1, 1),
        salary=50000.00,
        is_hr=False,
        is_active=True
    )
    test_employee.set_password('test123')
    test_employee.save()
    print(f"Created test employee: {test_employee.employee_id} with email: {test_employee.email}")
    
    # Test if we can authenticate
    if test_employee.check_password('test123'):
        print("Password verification successful!")
    else:
        print("Password verification failed!")
        
    # List all employees
    all_employees = Employee.objects.all()
    print(f"\nTotal employees in database: {all_employees.count()}")
    for emp in all_employees:
        print(f"ID: {emp.employee_id}, Email: {emp.email}, Name: {emp.first_name} {emp.last_name}")
        
except Exception as e:
    print(f"Error creating employee: {e}")
