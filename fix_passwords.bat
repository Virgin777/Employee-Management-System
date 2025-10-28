@echo off
cd /d "c:\Users\virgi\OneDrive\Desktop\Employee Management Systemsss"
call venv\Scripts\activate
cd backend
echo from employees.models import Employee; emp = Employee.objects.get(employee_id='EMP0001'); emp.set_password('emp123'); emp.save(); print(f'Password set for {emp.employee_id}'); emp2 = Employee.objects.get(employee_id='EMP0002'); emp2.set_password('emp123'); emp2.save(); print(f'Password set for {emp2.employee_id}') | python manage.py shell
pause
