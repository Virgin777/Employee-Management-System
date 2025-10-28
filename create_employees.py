# Script to create sample employees
from django.contrib.auth import get_user_model
from datetime import date

Employee = get_user_model()

# Create HR users
hr1, created = Employee.objects.get_or_create(
    employee_id='HR001',
    defaults={
        'email': 'hr.manager@company.com',
        'full_name': 'Sarah Johnson',
        'phone_number': '+1234567890',
        'date_of_birth': date(1985, 5, 15),
        'address': '123 Main St, City, State',
        'hire_date': date(2020, 1, 15),
        'department': 'HR',
        'designation': 'HR Manager',
        'salary': 75000.00,
        'is_hr': True,
        'is_active': True,
    }
)
if created:
    hr1.set_password('hr123')
    hr1.save()
    print(f'Created HR Manager: {hr1.email} (ID: {hr1.employee_id})')

hr2, created = Employee.objects.get_or_create(
    employee_id='HR002',
    defaults={
        'email': 'hr.assistant@company.com',
        'full_name': 'Mike Wilson',
        'phone_number': '+1234567891',
        'date_of_birth': date(1990, 8, 20),
        'address': '456 Oak Ave, City, State',
        'hire_date': date(2021, 3, 10),
        'department': 'HR',
        'designation': 'HR Assistant',
        'salary': 50000.00,
        'is_hr': True,
        'is_active': True,
    }
)
if created:
    hr2.set_password('hr123')
    hr2.save()
    print(f'Created HR Assistant: {hr2.email} (ID: {hr2.employee_id})')

# Create regular employees
employees_data = [
    {
        'employee_id': 'EMP001',
        'email': 'john.doe@company.com',
        'full_name': 'John Doe',
        'department': 'Engineering',
        'designation': 'Software Engineer',
        'salary': 80000.00,
    },
    {
        'employee_id': 'EMP002',
        'email': 'jane.smith@company.com',
        'full_name': 'Jane Smith',
        'department': 'Engineering',
        'designation': 'Senior Developer',
        'salary': 95000.00,
    },
    {
        'employee_id': 'EMP003',
        'email': 'bob.brown@company.com',
        'full_name': 'Bob Brown',
        'department': 'Sales',
        'designation': 'Sales Representative',
        'salary': 55000.00,
    },
    {
        'employee_id': 'EMP004',
        'email': 'alice.green@company.com',
        'full_name': 'Alice Green',
        'department': 'Marketing',
        'designation': 'Marketing Specialist',
        'salary': 60000.00,
    },
    {
        'employee_id': 'EMP005',
        'email': 'charlie.white@company.com',
        'full_name': 'Charlie White',
        'department': 'Finance',
        'designation': 'Financial Analyst',
        'salary': 70000.00,
    },
]

for emp_data in employees_data:
    employee, created = Employee.objects.get_or_create(
        employee_id=emp_data['employee_id'],
        defaults={
            'email': emp_data['email'],
            'full_name': emp_data['full_name'],
            'phone_number': '+1234567892',
            'date_of_birth': date(1988, 1, 1),
            'address': '789 Pine St, City, State',
            'hire_date': date(2022, 6, 1),
            'department': emp_data['department'],
            'designation': emp_data['designation'],
            'salary': emp_data['salary'],
            'is_hr': False,
            'is_active': True,
        }
    )
    if created:
        employee.set_password('emp123')
        employee.save()
        print(f'Created Employee: {employee.full_name} (ID: {employee.employee_id}, Email: {employee.email})')

print('\nSample employees created successfully!')
print('HR Users can login with email or employee ID:')
print('  - hr.manager@company.com or HR001 (password: hr123)')
print('  - hr.assistant@company.com or HR002 (password: hr123)')
print('\nEmployees can login with email or employee ID:')
print('  - john.doe@company.com or EMP001 (password: emp123)')
print('  - jane.smith@company.com or EMP002 (password: emp123)')
print('  - bob.brown@company.com or EMP003 (password: emp123)')
print('  - alice.green@company.com or EMP004 (password: emp123)')
print('  - charlie.white@company.com or EMP005 (password: emp123)')
