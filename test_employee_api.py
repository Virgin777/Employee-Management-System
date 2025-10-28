import requests
import json

def test_employee_creation():
    # Test data for creating employee
    employee_data = {
        "email": "test.employee@company.com",
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
    
    print("Testing employee creation API...")
    print("Data:", json.dumps(employee_data, indent=2))
    
    try:
        # Test without authentication first
        response = requests.post("http://localhost:8000/api/employees/", json=employee_data)
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        
        if response.status_code == 401:
            print("Authentication required - this is expected")
        elif response.status_code == 201:
            print("Employee created successfully!")
        else:
            print("Error occurred:")
            try:
                error_data = response.json()
                print("Error details:", json.dumps(error_data, indent=2))
            except:
                print("Raw error:", response.text)
                
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_employee_creation()
