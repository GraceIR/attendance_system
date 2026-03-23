# Attendance System

A Django-based attendance tracking system with AJAX, CSV export, and Bootstrap UI.

## Features
- Worker management
- Check-in with signature
- Date picker to view attendance history
- Edit/Delete records
- Export to CSV
- Responsive design

## Setup
1. Clone repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run server: `python manage.py runserver`

## Usage
- Add workers via admin panel.
- Use the main page to mark attendance.
