# SysPonto - Django Real-time Attendance System
This project is a web-based attendance management system built with Django, featuring distinct dashboards for students, teachers, and administrators, along with real-time notifications powered by Django Channels.
## [Quick Install Guide](https://github.com/pedrox86lopes/SysPonto-Attendance-Management-System/blob/main/docs/getting-started/installation.md)

![Deployed on Railway](https://railway.app/button.svg)

# 🚀 [Live Demo](https://sysponto-attendance-management-system-production.up.railway.app/)

## 🎮 Teachers and Students already created, just pick one:
- **Teachers:** `prof.silva`, `prof.santos`, `prof.costa` 
- **Students:** `student1` to `student8`
- **Password:** `password123` (for all accounts)

### Test Flow:
1. Login as teacher → Generate attendance code
2. Login as student → Enter code → Submit
3. See real-time updates in teacher dashboard

# Screenshots
## Login Page
![Image](https://github.com/user-attachments/assets/93ede926-3307-46b7-9563-69e8c9ad5cbd)

## Index Page
![Image](https://github.com/user-attachments/assets/2121bac1-5acd-4154-9075-ef49f2549370)

## Teacher Dashboard
![Image](https://github.com/user-attachments/assets/14b4a033-96aa-4772-8330-a28cbc90eff3)


![Screenshot from 2025-07-01 10-00-16](https://github.com/user-attachments/assets/1e9bc292-f740-4460-9742-ae00aa7ad762)

## Student Dashboard 
![Screenshot from 2025-07-01 10-00-48](https://github.com/user-attachments/assets/8b59e965-4435-421b-ba4a-495b29f1e69b)


![Screenshot from 2025-07-01 10-01-14](https://github.com/user-attachments/assets/d2c4ae51-98da-4c95-9331-33bbb024bd71)

## Student Justify Absence or later view

![Image](https://github.com/user-attachments/assets/389a1442-9124-4f4b-9fb4-08261c6401b9)

![Image](https://github.com/user-attachments/assets/2f4701c4-3f81-462b-a55e-48eec7eae996)

![Image](https://github.com/user-attachments/assets/ae45c5da-8619-404d-a858-e33eeca70b77)

## Absence Justification View in Django

![Image](https://github.com/user-attachments/assets/53810ed9-89d3-4d56-a894-83238032197f)

![Image](https://github.com/user-attachments/assets/0071e4f9-a9fd-4935-93dd-e66d95f3fdd7)
## Calendar 
![Image](https://github.com/user-attachments/assets/e786dc46-85d5-4609-92e2-55dd79d643cd)

## Database schema 
![Image](https://github.com/user-attachments/assets/25c6b363-7bce-42ac-a48f-c13e0efcc894)


# Features
User Authentication & Authorization: Secure login and role-based access for students, teachers, and admins.

# Student Dashboard:

View enrolled courses and upcoming class sessions.

Submit attendance codes for active classes.

Real-time notifications for attendance validation.

# Teacher Dashboard:

View classes they teach.

Generate unique, time-sensitive attendance codes (10-minute validity).

Receive real-time notifications when students submit attendance codes.

Validate student attendance submissions.

(Future) Display attendance statistics and plots (e.g., using Chart.js).

# Admin Dashboard:

Comprehensive user management (create, edit, delete students, teachers, and admins).

Course and class session creation and management.

(Future) Overall attendance reporting.

Real-time Notifications: Instant feedback and updates for teachers on student submissions, and for students on attendance validation, using Django Channels and WebSockets.

## Technology Stack
# Backend:
Python 3
<p>Django: The web framework.

<p>Django Channels: For asynchronous capabilities and WebSocket communication.

<p>Redis: Serves as the channel layer backend for Django Channels, enabling real-time messaging.
# Frontend:
HTML5

<p>CSS3 (with Bootstrap 5 for responsive design and components)

<p>JavaScript: For client-side logic, WebSocket handling, and dynamic UI updates.

# Database:
SQLite3 (default for development)

<p>PostgreSQL (recommended for production environments)
## Other Libraries:
asgiref: ASGI support.

<p>channels_redis: Redis backend for Channels.

# Setup Instructions
## Follow these steps to get the project up and running on your local machine.

## Prerequisites
Python 3.8+

<p>Django 4.0+

<p>PostgreSQL (or your preferred database)

## Redis Server:
Linux (Debian/Ubuntu): sudo apt update && sudo apt install redis-server

<p>macOS (Homebrew): brew install redis

## Windows: Refer to the official Redis documentation for installation.

## Ensure your Redis server is running before starting the Django application.

1. Clone the Repository
git clone <repository_url> # Replace with your actual repository URL
cd attendance_system

2. Create a Virtual Environment (Recommended)
python -m venv venv

3. Activate the Virtual Environment
macOS/Linux:

source venv/bin/activate

Windows:

.\venv\Scripts\activate

## 4. Install Dependencies
Install all required Python packages using pip:

pip install -r requirements.txt # Assuming you have a requirements.txt, or:

<p>pip install Django daphne channels channels_redis redis

## 5. Database Setup
Apply database migrations and create a superuser:

python manage.py makemigrations

<p>python manage.py migrate

<p>python manage.py createsuperuser # Follow prompts to create an admin user

## 6. Run the Development Server
Start the Django Channels development server using Daphne:


<p>daphne -b 0.0.0.0 -p 8000 attendance_system.asgi:application


<p>Your application should now be accessible at http://127.0.0.1:8000/.

# Populate with Test Data
cd attendance_system_django
<p> python manage.py create_test_data --clear
  
## Quick Reset for Fresh Testing:
python3 manage.py clean_database --confirm

Run again: <p> python manage.py create_test_data --clear

# Usage
## Access the Admin Panel: Log in as the superuser at http://127.0.0.1:8000/admin/ to:
Create Users (assign roles: student, teacher, admin).

<p>Create Courses.

<p>Create Class Sessions for courses.

<p>Enroll students in courses (Enrollment model).

# Student Dashboard:
Log in as a student.

<p>Navigate to /student/dashboard/.

<p>Enter attendance codes provided by the teacher for relevant classes. Notifications will appear upon successful submission and validation.

# Teacher Dashboard:
Log in as a teacher.

<p>Navigate to /teacher/dashboard/.

<p>Click "Generate New Code" for a class session. The code will appear and be valid for 10 minutes.

<p>Observe real-time notifications as students submit codes.

<p>Click "Validate" next to a student's name to confirm their attendance.

## Future Enhancements
Interactive Calendar: Fully integrate Calendar handling 30 days next of classes.


<p>Attendance Plots: Implement interactive statistical plots (e.g., bar charts of attendance frequency, line graphs over time) using libraries like Chart.js or Plotly.js.


<p>User Profile Management: Allow users to update their own profiles.


<p>Notifications UI: Enhance notification display with more visually appealing elements or a dedicated notification center.


<p>Search and Filtering: Add search and filter options for courses, classes, and attendance records in dashboards.


<p>Course Enrollment Workflow: Implement a student self-enrollment process.


<p>Email Notifications: Integrate email notifications for certain events (e.g., upcoming classes, attendance reports).
