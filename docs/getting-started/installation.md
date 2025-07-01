# Installation

## Quick Start on Linux
git clone https://github.com/pedrox86lopes/SysPonto-Attendance-Management-System.git
<p>cd SysPonto-Attendance-Management-System
<p>cd attendance_system_django
<p>python3 -m venv venv
<p>source venv/bin/activate
<p>pip install -r requirements.txt
  
## Set Up Database  
<p>python3 manage.py makemigrations 
<p>python3 manage.py migrate
<p>python3 manage.py createsuperuser # And follow the steps
  
<p>Run the server: daphne -b 0.0.0.0 -p 8000 attendance_system asgi:application
  
## Populate the Database with Fake Data
<p>python3 manage.py create_test_data
<p> You should see the output on the terminal showing the students/teachers with the usernames and a default password.
  
# Run the Development Server
Start the Django Channels development server using Daphne:

<p>daphne -b 0.0.0.0 -p 8000 attendance_system asgi:application

<p>Your application should now be accessible at http://127.0.0.1:8000/.

## Quick Start on Windows
<p> Prerequisites:
<p>Python 3.8+
<p>Git 
<p>git clone https://github.com/pedrox86lopes/SysPonto-Attendance-Management-System.git
<p>cd sysponto
<p>cd attendance_system_django

## Install Dependencies
<p>pip install django channels django-extensions
<p>or simply run the command: pip install -r requirements.txt
  
## Setup Database
<p>python manage.py makemigrations
<p>python manage.py migrate

## Create admin user (optional but recommended)
<p>python manage.py createsuperuser
  
## Populate the Database with Fake Data
<p>python3 manage.py create_test_data
<p> You should see the output on the terminal showing the students/teachers with the usernames and a default password.

## 👥 Default Login Credentials
<p>After running create_test_data, you can use these accounts:
  
## Teachers:
<p>Username: prof.silva | Password: password123
<p>Username: prof.santos | Password: password123
<p>Username: prof.costa | Password: password123

## Students:
<p>Username: student1 | Password: password123
<p>Username: student2 | Password: password123
<p>Username: student3 to student8 | Password: password123

# 🎯 Quick Testing Workflow
## For Teachers:
<p>Login with teacher credentials (e.g., prof.silva)
<p>Go to Teacher Dashboard
<p>Generate Code for a current class session
<p>Share the 6-digit code with students

## For Students:
<p>Login with student credentials (e.g., student1)
<p>Go to Student Dashboard
<p>Enter the attendance code provided by teacher
<p>Submit attendance (includes simulated location data)

# Real-time Features:
<p>Teachers see student submissions appear in real-time
<p>AI validation simulates fraud detection
<p>Teachers can approve/reject attendance

## 🛠 Additional Commands
<p>Reset Database (Clean Slate):
<p>bash# WARNING: This deletes all data except admin user
<p>python manage.py clean_database --confirm
  
## View Captured Data:
<p>bash# Shows attendance statistics
<p>python manage.py show_data
  
## Admin Panel:
<p>Visit: http://127.0.0.1:8000/admin/ - Check the current port you are hosting via daphne command.
<p>Login with superuser credentials

# 🔧 Troubleshooting
<p>Common Issues:
<p>"Python is not recognized"

<p>Reinstall Python and check "Add to PATH"
<p>Or use full path: C:\Python39\python.exe

<p>"Permission denied" errors

<p>Run Command Prompt as Administrator
<p>Or use PowerShell with execution policy: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Virtual environment not activating
<p>bash# Alternative activation method:
<p>venv\Scripts\Activate.ps1

# Or for Command Prompt:
<p>venv\Scripts\activate.bat
  
## Database errors
<p>bash# Delete database and recreate:
<p>del db.sqlite3
<p>python manage.py migrate
<p>python manage.py create_test_data
  
## 📱 How to Use
<p>Teacher Workflow:

<p>Login → Teacher Dashboard
<p>Select class session from dropdown
<p>Generate attendance code (6 characters, expires in 10 min)
<p>Share code with students
<p>Monitor real-time submissions
<p>Run AI validation on suspicious entries
<p>Approve attendance for students

## Student Workflow:

<p>Login → Student Dashboard
<p>Enter attendance code from teacher
<p>Submit (location automatically captured)
<p>Wait for teacher validation
<p>View attendance history

# Key Features:

✅ Real-time attendance tracking
✅ AI fraud detection simulation
✅ Geolocation validation
✅ Absence justification system
✅ Analytics dashboard
✅ Multi-course management

# 🌐 Access URLs

<p>Home Page: http://127.0.0.1:8000/
<p>Teacher Dashboard: http://127.0.0.1:8000/attendance/teacher/dashboard/
<p>Student Dashboard: http://127.0.0.1:8000/attendance/student/dashboard/
<p>Admin Panel: http://127.0.0.1:8000/admin/

# 🛑 Stopping the Server
<p>Press Ctrl + C in the command prompt to stop the development server.

