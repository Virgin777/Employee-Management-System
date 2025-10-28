from employees.models import Employee
from datetime import date

# Create a simple test employee
employee = Employee.objects.create_user(
    employee_id='TEST001',
    email='test@company.com',
    first_name='Test',
    last_name='User',
    phone='1234567890',
    department='IT',
    designation='Developer',
    date_of_joining=date(2023, 1, 1),
    salary=50000.00,
    password='test123'
)

print(f"Created employee: {employee.employee_id}")
print(f"Can login: {employee.check_password('test123')}")

# Also create an admin employee
admin_employee = Employee.objects.create_user(
    employee_id='ADMIN001',
    email='admin@company.com',
    first_name='Admin',
    last_name='User',
    phone='1234567891',
    department='HR',
    designation='Manager',
    date_of_joining=date(2023, 1, 1),
    salary=75000.00,
    is_hr=True,
    is_staff=True,
    password='admin123'
)

print(f"Created admin: {admin_employee.employee_id}")
print(f"Admin can login: {admin_employee.check_password('admin123')}")

# List all employees
print("\nAll employees:")
for emp in Employee.objects.all():
    print(f"ID: {emp.employee_id}, Email: {emp.email}, Name: {emp.first_name} {emp.last_name}, Active: {emp.is_active}")
