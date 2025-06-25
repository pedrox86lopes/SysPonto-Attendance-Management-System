# Installation

## Quick Start
git clone https://github.com/your-username/sysponto.git
<p>cd sysponto
<p>python -m venv venv
<p>source venv/bin/activate
<p>pip install -r requirements.txt
<p>python manage.py migrate
<p>python manage.py runserver

## Run the Development Server
Start the Django Channels development server using Daphne:

<p>daphne -b 0.0.0.0 -p 8000 attendance_system asgi:application

<p>Your application should now be accessible at http://127.0.0.1:8000/.

