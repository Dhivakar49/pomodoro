@echo off
echo Starting Django server...
call venv\Scripts\activate
start chrome http://127.0.0.1:8000/
python manage.py runserver
