Django Real-time Attendance System
This project is a web-based attendance management system built with Django, featuring distinct dashboards for students, teachers, and administrators, along with real-time notifications powered by Django Channels.

Features
User Authentication & Authorization: Secure login and role-based access for students, teachers, and admins.

Student Dashboard:

View enrolled courses and upcoming class sessions.

A calendar (placeholder for FullCalendar.js integration) to visualize their class schedule.

Submit attendance codes for active classes.

Real-time notifications for attendance validation.

Teacher Dashboard:

View classes they teach.

Generate unique, time-sensitive attendance codes (10-minute validity).

Receive real-time notifications when students submit attendance codes.

Validate student attendance submissions.

(Future) Display attendance statistics and plots (e.g., using Chart.js).

Admin Dashboard:

Comprehensive user management (create, edit, delete students, teachers, and admins).

Course and class session creation and management.

(Future) Overall attendance reporting.

Real-time Notifications: Instant feedback and updates for teachers on student submissions, and for students on attendance validation, using Django Channels and WebSockets.

Technology Stack
Backend:

Python 3

Django: The web framework.

Django Channels: For asynchronous capabilities and WebSocket communication.

Redis: Serves as the channel layer backend for Django Channels, enabling real-time messaging.

Frontend:

HTML5

CSS3 (with Bootstrap 5 for responsive design and components)

JavaScript: For client-side logic, WebSocket handling, and dynamic UI updates.

Database:

SQLite3 (default for development)

PostgreSQL (recommended for production environments)

Other Libraries:

asgiref: ASGI support.

channels_redis: Redis backend for Channels.

Setup Instructions
Follow these steps to get the project up and running on your local machine.

Prerequisites
Python 3.8+

pip (Python package installer)

Redis Server:

Linux (Debian/Ubuntu): sudo apt update && sudo apt install redis-server

macOS (Homebrew): brew install redis

Windows: Refer to the official Redis documentation for installation.

Ensure your Redis server is running before starting the Django application.

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

4. Install Dependencies
Install all required Python packages using pip:

pip install -r requirements.txt # Assuming you have a requirements.txt, or:
pip install Django daphne channels channels_redis redis

5. Database Setup
Apply database migrations and create a superuser:

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser # Follow prompts to create an admin user

6. Run the Development Server
Start the Django Channels development server using Daphne:

daphne -b 0.0.0.0 -p 8000 attendance_system.asgi:application

Your application should now be accessible at http://127.0.0.1:8000/.

Usage
Access the Admin Panel: Log in as the superuser at http://127.0.0.1:8000/admin/ to:

Create Users (assign roles: student, teacher, admin).

Create Courses.

Create Class Sessions for courses.

Enroll students in courses (Enrollment model).

Student Dashboard:

Log in as a student.

Navigate to /student/dashboard/.

Enter attendance codes provided by the teacher for relevant classes. Notifications will appear upon successful submission and validation.

Teacher Dashboard:

Log in as a teacher.

Navigate to /teacher/dashboard/.

Click "Generate New Code" for a class session. The code will appear and be valid for 10 minutes.

Observe real-time notifications as students submit codes.

Click "Validate" next to a student's name to confirm their attendance.

Project Structure (Key Directories)
attendance_system/
├── attendance_system/     # Main Django project settings
├── core/                  # Core user model and common utilities
├── courses/               # Models and views for Courses and Class Sessions
├── attendance/            # Models, views, consumers, and routing for attendance logic
│   ├── consumers.py       # WebSocket consumers for real-time communication
│   ├── models.py          # AttendanceCode, AttendanceRecord models
│   ├── routing.py         # WebSocket URL routing
│   └── views.py           # HTTP views for attendance submission/validation
├── templates/             # HTML templates (base, student, teacher dashboards)
├── static/                # Static files (CSS, JS)
└── media/                 # User-uploaded media (if applicable)

Future Enhancements
Interactive Calendar: Fully integrate FullCalendar.js on the student dashboard to display classes dynamically.

Attendance Plots: Implement interactive statistical plots (e.g., bar charts of attendance frequency, line graphs over time) using libraries like Chart.js or Plotly.js.

User Profile Management: Allow users to update their own profiles.

Notifications UI: Enhance notification display with more visually appealing elements or a dedicated notification center.

Search and Filtering: Add search and filter options for courses, classes, and attendance records in dashboards.

Course Enrollment Workflow: Implement a student self-enrollment process (if desired).

Email Notifications: Integrate email notifications for certain events (e.g., upcoming classes, attendance reports).
