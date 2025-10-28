import requests
import json

# Test the login API with the employee credentials
url = 'http://localhost:8000/api/auth/login/'

print("Testing Employee Login Authentication")
print("=" * 40)

# Test with EMP0001
test_data = {
    'email_or_employee_id': 'EMP0001',
    'password': 'emp123'  # Assuming you set this password
}

print("Testing login with EMP0001...")
try:
    response = requests.post(url, json=test_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ LOGIN SUCCESSFUL!")
        print(f"User: {result['user']['full_name']}")
        print(f"Employee ID: {result['user']['employee_id']}")
        print(f"Department: {result['user']['department']}")
        print(f"Access Token: {result['access'][:20]}...")
    else:
        print("❌ LOGIN FAILED!")
        print(f"Error: {response.json()}")
        
except requests.exceptions.ConnectionError:
    print("❌ Connection Error - Django server not running")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "-" * 40)

# Test with EMP0002
test_data2 = {
    'email_or_employee_id': 'EMP0002',
    'password': 'emp123'  # Assuming you set this password
}

print("Testing login with EMP0002...")
try:
    response = requests.post(url, json=test_data2)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ LOGIN SUCCESSFUL!")
        print(f"User: {result['user']['full_name']}")
        print(f"Employee ID: {result['user']['employee_id']}")
        print(f"Department: {result['user']['department']}")
    else:
        print("❌ LOGIN FAILED!")
        print(f"Error: {response.json()}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 40)
print("Authentication test completed!")
