import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')
django.setup()

from django.contrib.auth import get_user_model

Employee = get_user_model()

# Check existing HR users
print("Existing HR users:")
hr_users = Employee.objects.filter(is_hr=True)
for user in hr_users:
    print(f"- Email: {user.email}, Employee ID: {user.employee_id}, Active: {user.is_active}")

# Check if our test user exists
print("\nChecking for hr@example.com:")
try:
    test_user = Employee.objects.get(email='hr@example.com')
    print(f"Found: {test_user.email} (ID: {test_user.employee_id}, HR: {test_user.is_hr})")
except Employee.DoesNotExist:
    print("hr@example.com does not exist")
    
    # Create test HR user
    print("Creating test HR user...")
    test_user = Employee.objects.create_user(
        employee_id='HR999',
        email='hr@example.com',
        password='admin123',
        first_name='Test',
        last_name='HR',
        phone='1234567890',
        department='HR',
        designation='HR Manager',
        date_of_joining='2025-01-01',
        salary=75000,
        is_hr=True,
        is_active=True
    )
    print(f"Created test HR user: {test_user.email}")
