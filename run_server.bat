@echo off
cd /d "c:\Users\virgi\OneDrive\Desktop\Employee Management Systemsss"
call venv\Scripts\activate
cd backend
echo "Running Django management command..."
python manage.py runserver 0.0.0.0:8000
