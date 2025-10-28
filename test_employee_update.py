#!/usr/bin/env python3

import requests
import json

def test_employee_update():
    base_url = "http://localhost:8000"
    
    # Login as HR user
    print("Logging in as HR...")
    login_data = {
        "email_or_employee_id": "admin@example.com",
        "password": "admin123"
    }
    
    response = requests.post(f"{base_url}/api/auth/token-login/", json=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.status_code} - {response.text}")
        return
    
    auth_data = response.json()
    token = auth_data.get('token')
    headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
    
    # Get list of employees to find one to update
    print("Getting employee list...")
    employees_response = requests.get(f"{base_url}/api/employees/", headers=headers)
    if employees_response.status_code != 200:
        print(f"Failed to get employees: {employees_response.status_code}")
        return
    
    employees = employees_response.json()
    print(f"Employees response type: {type(employees)}")
    print(f"Employees response: {employees}")
    
    if not employees:
        print("No employees found")
        return
    
    # Handle both list and paginated response formats
    if isinstance(employees, dict) and 'results' in employees:
        employees = employees['results']
    
    # Find a non-admin employee to update
    test_employee = None
    for emp in employees:
        print(f"Employee: {emp}")
        if isinstance(emp, dict) and emp.get('email') != 'admin@example.com':
            test_employee = emp
            break
    
    if not test_employee:
        print("No suitable employee found for testing")
        return
    
    employee_id = test_employee['id']
    print(f"Testing update for employee ID: {employee_id}")
    print(f"Current employee data: {json.dumps(test_employee, indent=2)}")
    
    # Try to update the employee
    update_data = {
        "first_name": test_employee.get('first_name', 'Test'),
        "last_name": test_employee.get('last_name', 'User'), 
        "phone": test_employee.get('phone', '1234567890'),
        "department": test_employee.get('department', 'IT'),
        "designation": test_employee.get('designation', 'Developer'),
        "date_of_joining": test_employee.get('date_of_joining', '2025-01-01'),
        "salary": 60000.00,
        "is_hr": test_employee.get('is_hr', False)
    }
    
    print(f"Update data: {json.dumps(update_data, indent=2)}")
    
    update_response = requests.put(f"{base_url}/api/employees/{employee_id}/", json=update_data, headers=headers)
    print(f"Update response status: {update_response.status_code}")
    print(f"Update response: {update_response.text}")
    
    if update_response.status_code == 200:
        print("Update successful!")
    else:
        print("Update failed!")
        try:
            error_data = update_response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print("Could not parse error response as JSON")

if __name__ == "__main__":
    test_employee_update()
