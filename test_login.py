import requests
import json

# Test the login API
url = 'http://localhost:8000/api/auth/login/'

# First, let's test with different combinations to see what works
test_cases = [
    {
        'name': 'Test with admin email',
        'data': {
            'email_or_employee_id': 'admin@example.com',
            'password': 'admin123'
        }
    },
    {
        'name': 'Test with admin employee ID',
        'data': {
            'email_or_employee_id': 'ADMIN001',
            'password': 'admin123'
        }
    },
    {
        'name': 'Test with EMP001',
        'data': {
            'email_or_employee_id': 'EMP001',
            'password': 'emp123'
        }
    },
    {
        'name': 'Test with test user',
        'data': {
            'email_or_employee_id': 'TEST001',
            'password': 'test123'
        }
    }
]

for test_case in test_cases:
    print(f"\n{test_case['name']}...")
    try:
        response = requests.post(url, json=test_case['data'])
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS!")
            print(f"Response: {response.json()}")
        else:
            print(f"Error Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Connection Error - Django server might not be running")
    except Exception as e:
        print(f"Error: {e}")

# Also test the user listing endpoint if it exists
print("\n" + "="*50)
print("Testing user list endpoint...")
try:
    response = requests.get('http://localhost:8000/api/employees/')
    print(f"Employees endpoint status: {response.status_code}")
    if response.status_code == 200:
        employees = response.json()
        print(f"Found {len(employees)} employees")
        for emp in employees[:3]:  # Show first 3
            print(f"- ID: {emp.get('employee_id')}, Email: {emp.get('email')}")
except Exception as e:
    print(f"Error accessing employees endpoint: {e}")
