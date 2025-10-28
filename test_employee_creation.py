import requests
import json

# Test employee creation
def test_employee_creation():
        # First, login as HR user
    print("Testing HR login...")
    login_data = {
        "email_or_employee_id": "admin@example.com",
        "password": "admin123"
    }
    
    login_response = requests.post("http://localhost:8000/api/auth/login/", json=login_data)
    print("Login response status:", login_response.status_code)
    print("Login response:", login_response.json())
    
    if login_response.status_code == 200:
        token = login_response.json()['token']
        headers = {'Authorization': f'Token {token}'}
        
        # Test employee data
        employee_data = {
            "email": "test.employee@example.com",
            "first_name": "Test",
            "last_name": "Employee",
            "phone": "1234567890",
            "department": "IT",
            "designation": "Developer",
            "date_of_joining": "2025-08-27",
            "salary": 50000,
            "password": "testpass123",
            "is_hr": False
        }
        
        print("\nCreating employee with data:")
        print(json.dumps(employee_data, indent=2))
        
        response = requests.post("http://localhost:8000/api/employees/", json=employee_data, headers=headers)
        print(f"\nEmployee creation response status: {response.status_code}")
        print("Employee creation response:")
        print(response.text)
        
        if response.status_code != 201:
            print("Error details:", response.json() if response.content else "No content")
    else:
        print("Login failed!")

if __name__ == "__main__":
    test_employee_creation()
