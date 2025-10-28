@echo off
cd /d "c:\Users\virgi\OneDrive\Desktop\Employee Management Systemsss"
call venv\Scripts\activate
cd backend
python manage.py create_sample_employees
pause
