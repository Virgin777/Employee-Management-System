import requests
import json

# Test login with the employee ID from the screenshot
url = 'http://localhost:8000/api/auth/login/'

# Test with EMP0001 (as shown in the frontend login attempt)
test_data = {
    'email_or_employee_id': 'EMP0001',
    'password': 'your_stored_password_here'  # Replace with actual password
}

print("Testing login with EMP0001...")
try:
    response = requests.post(url, json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Also test if we can retrieve employee info
print("\nTesting if employee exists...")
try:
    # Test if employee exists by checking the employees endpoint
    response = requests.get('http://localhost:8000/api/employees/')
    print(f"Employees list status: {response.status_code}")
    if response.status_code == 200:
        employees = response.json()
        for emp in employees:
            if emp.get('employee_id') == 'EMP0001':
                print(f"Found employee: {emp}")
                break
        else:
            print("EMP0001 not found in employees list")
except Exception as e:
    print(f"Error accessing employees: {e}")
