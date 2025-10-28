import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append('c:/Users/virgi/OneDrive/Desktop/Employee Management Systemsss/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')
django.setup()

from employees.models import Employee

# Check what employees exist and their exact details
print("Checking existing employees in database:")
print("=" * 50)

employees = Employee.objects.all()
for emp in employees:
    print(f"Employee ID: '{emp.employee_id}'")
    print(f"Email: '{emp.email}'")
    print(f"First Name: '{emp.first_name}'")
    print(f"Last Name: '{emp.last_name}'")
    print(f"Is Active: {emp.is_active}")
    print(f"Has Password: {bool(emp.password)}")
    print(f"Password Hash: {emp.password[:20]}..." if emp.password else "No password set")
    print("-" * 30)

# Test password checking for EMP0001 specifically
try:
    emp = Employee.objects.get(employee_id='EMP0001')
    print(f"\nFound EMP0001:")
    print(f"Email: {emp.email}")
    print(f"Active: {emp.is_active}")
    print(f"Password set: {bool(emp.password)}")
    
    # Test with common passwords
    test_passwords = ['admin123', 'password', '123456', 'emp123', 'employee123']
    for pwd in test_passwords:
        if emp.check_password(pwd):
            print(f"✓ Password '{pwd}' works!")
            break
    else:
        print("✗ None of the common passwords work")
        
except Employee.DoesNotExist:
    print("EMP0001 not found in database")
except Exception as e:
    print(f"Error: {e}")
