@echo off
cd /d "c:\Users\virgi\OneDrive\Desktop\Employee Management Systemsss"
call venv\Scripts\activate
cd backend
echo Creating sample employees...
python manage.py create_sample_employees
echo Done!
