# SysPonto - Django Real-time Attendance System
This project is a web-based attendance management system built with Django, featuring distinct dashboards for students, teachers, and administrators, along with real-time notifications powered by Django Channels.

# Screenshots
## Login Page
![Image](https://github.com/user-attachments/assets/93ede926-3307-46b7-9563-69e8c9ad5cbd)

## Index Page
![Image](https://github.com/user-attachments/assets/2121bac1-5acd-4154-9075-ef49f2549370)

## Teacher Dashboard
![Image](https://github.com/user-attachments/assets/998d17aa-b7f0-4046-8750-81b4bb85bbb9)


![Image](https://github.com/user-attachments/assets/4ce96d0b-f79c-4b32-a20c-7d0ac711e596)

## Student Dashboard 
![Image](https://github.com/user-attachments/assets/f7582b88-6900-405b-95ed-c6a99c230bb5)


![Image](https://github.com/user-attachments/assets/cec7408b-950b-4f27-841a-bd6206a10746)

## Student Justify Absence or later view

![Image](https://github.com/user-attachments/assets/389a1442-9124-4f4b-9fb4-08261c6401b9)

![Image](https://github.com/user-attachments/assets/2f4701c4-3f81-462b-a55e-48eec7eae996)

![Image](https://github.com/user-attachments/assets/ae45c5da-8619-404d-a858-e33eeca70b77)

## Absence Justification View in Django

![Image](https://github.com/user-attachments/assets/53810ed9-89d3-4d56-a894-83238032197f)

![Image](https://github.com/user-attachments/assets/0071e4f9-a9fd-4935-93dd-e66d95f3fdd7)
## Calendar 
![Image](https://github.com/user-attachments/assets/e786dc46-85d5-4609-92e2-55dd79d643cd)

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
Django: The web framework.
Django Channels: For asynchronous capabilities and WebSocket communication.
Redis: Serves as the channel layer backend for Django Channels, enabling real-time messaging.
# Frontend:
HTML5
CSS3 (with Bootstrap 5 for responsive design and components)
JavaScript: For client-side logic, WebSocket handling, and dynamic UI updates.

# Database:
SQLite3 (default for development)
PostgreSQL (recommended for production environments)
## Other Libraries:
asgiref: ASGI support.
channels_redis: Redis backend for Channels.

# Setup Instructions
## Follow these steps to get the project up and running on your local machine.

## Prerequisites
Python 3.8+
Django 4.0+
PostgreSQL (or your preferred database)

## Redis Server:
Linux (Debian/Ubuntu): sudo apt update && sudo apt install redis-server
macOS (Homebrew): brew install redis

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
pip install Django daphne channels channels_redis redis

## 5. Database Setup
Apply database migrations and create a superuser:

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser # Follow prompts to create an admin user

## 6. Run the Development Server
Start the Django Channels development server using Daphne:

daphne -b 0.0.0.0 -p 8000 attendance_system.asgi:application

Your application should now be accessible at http://127.0.0.1:8000/.

# Usage
## Access the Admin Panel: Log in as the superuser at http://127.0.0.1:8000/admin/ to:
Create Users (assign roles: student, teacher, admin).
Create Courses.
Create Class Sessions for courses.
Enroll students in courses (Enrollment model).

# Student Dashboard:
Log in as a student.
Navigate to /student/dashboard/.
Enter attendance codes provided by the teacher for relevant classes. Notifications will appear upon successful submission and validation.

# Teacher Dashboard:
Log in as a teacher.
Navigate to /teacher/dashboard/.
Click "Generate New Code" for a class session. The code will appear and be valid for 10 minutes.
Observe real-time notifications as students submit codes.
Click "Validate" next to a student's name to confirm their attendance.

## Future Enhancements
Interactive Calendar: Fully integrate FullCalendar.js on the student dashboard to display classes dynamically.

Attendance Plots: Implement interactive statistical plots (e.g., bar charts of attendance frequency, line graphs over time) using libraries like Chart.js or Plotly.js.

User Profile Management: Allow users to update their own profiles.

Notifications UI: Enhance notification display with more visually appealing elements or a dedicated notification center.

Search and Filtering: Add search and filter options for courses, classes, and attendance records in dashboards.

Course Enrollment Workflow: Implement a student self-enrollment process (if desired).

Email Notifications: Integrate email notifications for certain events (e.g., upcoming classes, attendance reports).
