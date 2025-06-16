# attendance/views.py
import json
import random
import math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime, timedelta
from django.urls import reverse
from django.db.models import Q 
from django.utils.timezone import localdate
import logging



# Import your models
from core.models import User
from courses.models import Course, ClassSession
from attendance.models import AttendanceCode, AttendanceRecord, Enrollment


# Helper function to send notification to a group
def send_group_notification(group_name, message_type, message, context={}):
    """
    Sends a message to a specific Channel Layer group.
    The 'type' key in the message dict must match a method name in your consumer.
    """
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': message_type, # This now dynamically sets the method name in consumer
                'message': message,
                'context': context,
            }
        )

# --- Role-based access decorators ---
def is_teacher(user):
    """Checks if the logged-in user is a teacher."""
    return user.is_authenticated and user.role == 'teacher'

def is_student(user):
    """Checks if the logged-in user is a student."""
    return user.is_authenticated and user.role == 'student'

def is_admin(user):
    """Checks if the logged-in user is an admin."""
    return user.is_authenticated and user.role == 'admin'

# --- Teacher Views ---

@login_required(login_url='/login/')
@user_passes_test(is_teacher, login_url='/login/')
def teacher_portal(request):
    """
    Renders the teacher portal landing page (equivalent to Next.js teacher/page.tsx).
    Provides navigation options for teachers.
    """
    return render(request, 'teacher/teacher_portal.html')

@login_required(login_url='/login/')
@user_passes_test(is_teacher, login_url='/login/')
def teacher_generate_code(request):
    """
    Renders the page for teachers to generate attendance codes (equivalent to
    Next.js teacher/generate-code/page.tsx).
    It pre-loads any currently active or recently expired code for the teacher's
    classes today.
    """
    today = localdate()
    current_code_details = {'code_status': 'inactive', 'code': None, 'class_session_id': None, 'expires_at': None}

    class_sessions_today = ClassSession.objects.filter(
        course__teachers=request.user,
        date=today
    ).order_by('start_time').select_related('course')

    # Try to find an active or recently expired code for today's sessions
    found_code_for_display = False
    for session in class_sessions_today:
        try:
            code_obj = AttendanceCode.objects.get(class_session=session)
            if code_obj.is_valid():
                current_code_details = {
                    'code': code_obj.code,
                    'class_session_id': str(session.id), # Ensure it's a string
                    'expires_at': code_obj.expires_at.isoformat(),
                    'code_status': 'active'
                }
                found_code_for_display = True
                break # Stop searching, we found an active one
            else:
                # If not active, but we haven't found an active one yet,
                # keep this expired one as the potential display
                if not found_code_for_display:
                     current_code_details = {
                        'code': code_obj.code,
                        'class_session_id': str(session.id), # Ensure it's a string
                        'expires_at': code_obj.expires_at.isoformat(),
                        'code_status': 'expired'
                    }
        except AttendanceCode.DoesNotExist:
            pass # No code for this session, continue

    # IMPORTANT: If no code (active or expired) was found, but the teacher has classes today,
    # set a default class_session_id for the UI to use when generating a new code.
    if not current_code_details['class_session_id'] and class_sessions_today.exists():
        # Pick the first class session for today as the default target for code generation
        current_code_details['class_session_id'] = str(class_sessions_today.first().id)
        # Also set the course name for the initial display if you want (optional)
        # current_code_details['course_name'] = class_sessions_today.first().course.name

    return render(request, 'teacher/teacher_generate_code.html', {
        'initial_code_details': json.dumps(current_code_details)
    })


@login_required(login_url='/login/')
@user_passes_test(is_teacher, login_url='/login/')
@require_POST # This view only accepts POST requests
def generate_attendance_code(request):
    """
    API endpoint for teachers to generate a new attendance code for a SELECTED class.
    Now expects a 'class_session_id' in the POST request from the form.
    """
    class_session_id = request.POST.get('class_session_id')
    if not class_session_id:
        return JsonResponse({'status': 'error', 'message': 'Class session ID is required.'}, status=400)

    try:
        target_class_session = ClassSession.objects.get(id=class_session_id)
        # Verify the teacher is associated with this class's course
        if not target_class_session.course.teachers.filter(id=request.user.id).exists():
            return JsonResponse({'status': 'error', 'message': 'Permission denied: Not your class.'}, status=403)

        # Check if the class is today and is ongoing or upcoming
        today = localdate()
        now_time = timezone.now().time()
        # Comparing date objects for 'date' field, and time objects for 'end_time'
        if target_class_session.date != today or target_class_session.end_time < now_time:
             return JsonResponse({'status': 'error', 'message': 'Cannot generate code for past or non-today class.'}, status=400)


    except ClassSession.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Class session not found.'}, status=404)

    # Invalidate any existing attendance code for this specific session
    # This ensures only one code is active per session at any time
    AttendanceCode.objects.filter(class_session=target_class_session, expires_at__gte=timezone.now()).update(expires_at=timezone.now() - timedelta(minutes=1))

    # Generate a new random code (Example: 6 characters alphanumeric)
    import secrets
    import string
    characters = string.ascii_uppercase + string.digits
    new_code_value = ''.join(secrets.choice(characters) for _ in range(6))
    expires_at = timezone.now() + timedelta(minutes=10)

    # This will either get the existing code for this session and update it,
    # or create a new one if it doesn't exist.
    new_code_obj, created = AttendanceCode.objects.update_or_create(
        class_session=target_class_session, # This is the unique identifier for update_or_create
        defaults={ # These are the fields to update or set for a new object
            'code': new_code_value,
            'expires_at': expires_at,
            'generated_by': request.user,
        }
    )

    # Send a real-time notification to the class session group (for Teacher Dashboard)
    # The dashboard's WebSocket listens to this group for its real-time updates.
    send_group_notification(
        group_name=f'class_session_{target_class_session.id}_notifications', # Target the class session group
        message_type='code_generated_for_teacher', # Specific message type for frontend
        message=f"New code '{new_code_obj.code}' generated for {target_class_session.course.name}!",
        context={
            'code': new_code_obj.code,
            'class_session_id': str(target_class_session.id), # Ensure ID is string for JS consistency
            'expires_at': new_code_obj.expires_at.isoformat(), # Send in ISO format for JS
            'code_status': 'active'
        }
    )

    return JsonResponse({
        'status': 'success',
        'code': new_code_obj.code,
        'class_session_id': str(target_class_session.id), # Ensure ID is string for JS consistency
        'expires_at': new_code_obj.expires_at.isoformat(), # Return this to the client
    })


@login_required(login_url='/login/')
@user_passes_test(is_teacher, login_url='/login/')
def teacher_dashboard(request):
    """
    Renders the teacher's attendance dashboard.
    Fetches all ongoing/upcoming classes for the teacher today,
    and initial data for the most relevant class session.
    """
    today = localdate()
    now_time = timezone.now().time()

    teacher_class_sessions_today = ClassSession.objects.filter(
        Q(start_time__lte=now_time, end_time__gte=now_time) | Q(start_time__gt=now_time),
        course__teachers=request.user,
        date=today
    ).order_by('start_time').select_related('course')

    current_code_details = {'code_status': 'inactive', 'code': None, 'class_session_id': None, 'expires_at': None}
    student_submissions_data = []
    active_class_session_for_display = None

    for session in teacher_class_sessions_today:
        try:
            code_obj = AttendanceCode.objects.get(class_session=session)
            if code_obj.is_valid():
                active_class_session_for_display = session
                current_code_details = {
                    'code': code_obj.code,
                    'class_session_id': str(session.id),
                    'expires_at': code_obj.expires_at.isoformat(),
                    'code_status': 'active'
                }
                break
        except AttendanceCode.DoesNotExist:
            pass

    if not active_class_session_for_display and teacher_class_sessions_today.exists():
        active_class_session_for_display = teacher_class_sessions_today.first()
        try:
            expired_code_obj = AttendanceCode.objects.get(class_session=active_class_session_for_display)
            current_code_details = {
                'code': expired_code_obj.code,
                'class_session_id': str(expired_code_obj.class_session.id),
                'expires_at': expired_code_obj.expires_at.isoformat(),
                'code_status': 'expired'
            }
        except AttendanceCode.DoesNotExist:
            current_code_details = {
                'code_status': 'inactive',
                'code': None,
                'class_session_id': str(active_class_session_for_display.id),
                'expires_at': None
            }

    if active_class_session_for_display:
        submissions = AttendanceRecord.objects.filter(
            class_session=active_class_session_for_display
        ).select_related('student').order_by('timestamp')
        
        for sub in submissions:
            ai_result_data = None
            # Assuming ai_result_json is the field name that stores the JSON string
            if hasattr(sub, 'ai_result_json') and sub.ai_result_json: 
                try:
                    ai_result_data = json.loads(sub.ai_result_json)
                except json.JSONDecodeError:
                    logger = logging.getLogger(__name__)
                    logger.warning("Could not decode AI result JSON for record ID %s", sub.id)

            student_submissions_data.append({
                'id': sub.id,
                'name': sub.student.get_full_name() or sub.student.username,
                'timestamp': sub.timestamp.isoformat(),
                'simulatedIp': sub.simulated_ip,
                'simulatedGeolocation': sub.simulated_geolocation,
                'aiResult': ai_result_data,
                'is_present': sub.is_present,
            })

    # Known valid locations (hardcoded for now, can come from model/settings in production)
    known_valid_locations = [
        {"latitude": 41.5369, "longitude": -8.4239}, # Example coordinates for CESAE Digital (Braga)
    ]

    context = {
        'teacher_class_sessions_today': teacher_class_sessions_today, # All classes for today for the dropdown
        'active_class_session_for_display': active_class_session_for_display, # The one whose submissions are initially shown
        'initial_code_details': json.dumps(current_code_details),
        'initial_student_submissions': json.dumps(student_submissions_data),
        'known_valid_locations': json.dumps(known_valid_locations),
        # Pass the ID of the active session so JS knows which channel to listen to for student submissions
        'active_class_session_id': str(active_class_session_for_display.id) if active_class_session_for_display else None
    }
    return render(request, 'teacher/teacher_dashboard.html', context)


@login_required(login_url='/login/')
@user_passes_test(is_teacher, login_url='/login/')
@require_POST
def run_ai_validation(request):
    """
    API endpoint for teachers to trigger AI validation on a specific attendance record.
    Simulates AI logic (random outcome, basic geolocation check).
    """
    attendance_record_id = request.POST.get('attendance_record_id')
    class_session_id = request.POST.get('class_session_id') # Used for authorization check

    if not attendance_record_id or not class_session_id:
        return JsonResponse({'status': 'error', 'message': 'Record ID and Class Session ID are required.'}, status=400)

    try:
        record = AttendanceRecord.objects.get(id=attendance_record_id, class_session__id=class_session_id)
        # Ensure the teacher is authorized for this record's class
        if not record.class_session.course.teachers.filter(id=request.user.id).exists():
            return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)

    except AttendanceRecord.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Attendance record not found.'}, status=404)

    # --- Simulate AI Logic (Enhanced) ---
    is_fraudulent = False
    fraud_explanation = "No issues detected."

    # More sophisticated random fraud detection
    if random.random() < 0.2: # 20% chance of random fraud
        is_fraudulent = True
        fraud_explanation = random.choice([
            "Unusual activity pattern detected.",
            "Potential VPN usage identified.",
            "High velocity movement detected."
        ])

    # Geolocation check
    if record.simulated_geolocation: # This field should be a JSONField or similar
        sim_lat = record.simulated_geolocation.get('latitude')
        sim_lon = record.simulated_geolocation.get('longitude')
        
        # Define the primary valid location (e.g., CESAE Digital)
        cesae_lat = 41.5431
        cesae_lon = -8.4079

        # Simple distance check (using approximate degree-to-km conversion for small distances)
        # 1 degree lat is approx 111 km, 1 degree lon is approx 111*cos(lat) km
        # Added math.radians for correct cosine calculation
        if sim_lat is not None and sim_lon is not None:
            lat_diff = abs(sim_lat - cesae_lat) * 111
            lon_diff = abs(sim_lon - cesae_lon) * 111 * abs(math.cos(math.radians(cesae_lat))) 

            if lat_diff > 0.5 or lon_diff > 0.5: # If distance is > 0.5 km
                is_fraudulent = True
                fraud_explanation = "Geolocation is outside the expected classroom area."
        else:
            is_fraudulent = True
            fraud_explanation = "Incomplete geolocation data provided."
    else:
        # If no geolocation provided, consider it suspicious for AI check
        is_fraudulent = True
        fraud_explanation = "Geolocation data missing or could not be obtained."

    # Store AI result as a JSON string
    ai_result_dict = {
        'isFraudulent': is_fraudulent,
        'fraudExplanation': fraud_explanation
    }
    record.ai_result_json = json.dumps(ai_result_dict) # Ensure this matches your model field name
    record.save()

    # Send real-time notification to the class session group for dashboard update
    send_group_notification(
        group_name=f'class_session_{class_session_id}_notifications',
        message_type='ai_result_updated_for_teacher', # New message type for frontend
        message=f"AI validation run for record {attendance_record_id}.",
        context={
            'record_id': str(record.id),
            'aiResult': ai_result_dict, # Send the dictionary directly
            'class_session_id': str(class_session_id),
        }
    )

    return JsonResponse({
        'status': 'success',
        'aiResult': ai_result_dict, # Return the dictionary
        'attendance_record_id': str(record.id)
    })


@login_required(login_url='/login/')
@user_passes_test(is_teacher, login_url='/login/')
@require_POST
def validate_attendance(request):
    """
    API endpoint for teachers to validate a student's attendance submission.
    Marks the attendance record as 'present'.
    """
    attendance_record_id = request.POST.get('attendance_record_id')
    if not attendance_record_id:
        return JsonResponse({'status': 'error', 'message': 'Attendance record ID is required.'}, status=400)

    try:
        attendance_record = AttendanceRecord.objects.get(id=attendance_record_id)
        # Ensure this teacher is validating for a class they teach
        if not attendance_record.class_session.course.teachers.filter(id=request.user.id).exists():
            return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)

    except AttendanceRecord.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Attendance record not found.'}, status=404)

    attendance_record.is_present = True
    attendance_record.save()

    # Send Notification to the specific Student whose attendance was validated (personal group)
    student_group_name = f'user_{attendance_record.student.id}_notifications'
    send_group_notification(
        group_name=student_group_name,
        message_type='attendance_validated',
        message=f"Your attendance for {attendance_record.class_session.course.name} on {attendance_record.class_session.date.strftime('%Y-%m-%d')} has been validated!",
        context={
            'class_name': str(attendance_record.class_session.course.name), # Use course name
            'status': 'present',
            'record_id': str(attendance_record.id),
            'class_session_id': str(attendance_record.class_session.id),
        }
    )
    
@login_required(login_url='/login/')
@user_passes_test(is_teacher, login_url='/login/')
@require_GET # This view only accepts GET requests
def get_session_submissions(request):
    """
    API endpoint to fetch attendance submissions for a specific class session.
    """
    class_session_id = request.GET.get('class_session_id')
    if not class_session_id:
        return JsonResponse({'status': 'error', 'message': 'Class session ID is required.'}, status=400)

    try:
        class_session = ClassSession.objects.get(id=class_session_id)
        # Verify the teacher is associated with this class's course
        if not class_session.course.teachers.filter(id=request.user.id).exists():
            return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)

    except ClassSession.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Class session not found.'}, status=404)

    submissions = AttendanceRecord.objects.filter(
        class_session=class_session
    ).select_related('student').order_by('timestamp')

    student_submissions_data = []
    for sub in submissions:
        ai_result_data = None
        if hasattr(sub, 'ai_result_json') and sub.ai_result_json:
            try:
                ai_result_data = json.loads(sub.ai_result_json)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode AI result JSON for record ID {sub.id}")
                ai_result_data = None

        student_submissions_data.append({
            'id': str(sub.id), # Ensure ID is string for JS
            'name': sub.student.get_full_name() or sub.student.username,
            'timestamp': sub.timestamp.isoformat(),
            'simulatedIp': sub.simulated_ip,
            'simulatedGeolocation': sub.simulated_geolocation,
            'aiResult': ai_result_data,
            'is_present': sub.is_present,
            'class_session_id': str(class_session.id),
        })

    return JsonResponse({'status': 'success', 'submissions': student_submissions_data})

# --- Student Views ---

@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
def student_dashboard(request):
    # Get the current student (request.user)
    # The `course__course_enrollments__student=request.user` filter works for this.

    today = localdate() # Get today's date in the user's local timezone (Europe/Lisbon)
    now_local_time = timezone.localtime().time() # Get current time (e.g., 11:58:23) in the user's local timezone
    

    # Debugging: Uncomment these lines to see the exact time values Django is using
    # print(f"DEBUG: Today's date (local): {today}")
    # print(f"DEBUG: Current time (local): {now_local_time}")


    # --- Fetching Enrolled Courses ---
    # This will get a distinct list of all courses the student is enrolled in.
    enrolled_courses_qs = Course.objects.filter(course_enrollments__student=request.user).distinct()


    # --- Fetching Today's Classes (ALL classes for today for the enrolled courses) ---
    # This will get every class session scheduled for today, regardless of start/end time.
    # This is what you want to match the calendar's full day view.
    today_sessions = ClassSession.objects.filter(
        course__course_enrollments__student=request.user, # Filter by courses the student is enrolled in
        date=today, # Only sessions scheduled for today
    ).order_by('start_time').select_related('course') # Order by start time for display, optimize with select_related


    # --- Fetching Next Upcoming Class (The very next class from the current moment onwards) ---
    # This will find the single class session that is closest in the future.
    next_upcoming_session = ClassSession.objects.filter(
        course__course_enrollments__student=request.user # Filter by courses the student is enrolled in
    ).filter(
        # Use Q objects for an OR condition:
        # (1) Sessions today that start AFTER the current local time, OR
        # (2) Sessions on any future date (tomorrow or later).
        Q(date=today, start_time__gt=now_local_time) | Q(date__gt=today)
    ).order_by('date', 'start_time').select_related('course').first() # Get only the very first matching session


    context = {
        'enrolled_courses': enrolled_courses_qs,
        'today_sessions': today_sessions,
        'next_upcoming_session': next_upcoming_session,
    }
    return render(request, 'student/student_dashboard.html', context) # Ensure correct template path


@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
def student_portal(request):
    """
    Renders the student portal landing page.
    """
    return render(request, 'student/student_portal.html')

@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
def student_enter_code(request):
    """
    Renders the page where students can enter attendance codes.
    """
    return render(request, 'student/student_enter_code.html')

@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
@require_GET
def student_calendar(request):
    """
    Renders the student's calendar page.
    Fetches and formats enrolled class sessions for FullCalendar.js.
    """
    # by the current user's enrollments.
    enrolled_class_sessions = ClassSession.objects.filter(
        course__course_enrollments__student=request.user, 
        date__gte=timezone.localdate() # Show upcoming classes from today onwards
    ).order_by('date', 'start_time').select_related('course')

    # Format events for FullCalendar.js
    calendar_events = []
    for session in enrolled_class_sessions:
        calendar_events.append({
            'title': session.course.name,
            'start': f"{session.date.isoformat()}T{session.start_time.isoformat()}",
            'end': f"{session.date.isoformat()}T{session.end_time.isoformat()}",
            'id': session.id,
        })

    return render(request, 'student/student_calendar.html', {
        'calendar_events_json': json.dumps(calendar_events) # Pass as JSON string
    })

@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
@require_POST
def submit_attendance_code(request):
    """
    API endpoint for students to submit an attendance code.
    Validates the code and creates an AttendanceRecord.
    """
    code = request.POST.get('attendance_code').strip().upper() # Clean and standardize code
    # class_session_id is not directly used for lookup but can be passed for context if needed

    if not code:
        return JsonResponse({'status': 'error', 'message': 'Attendance code is required.'}, status=400)

    try:
        # Get the code and ensure it's linked to a class session
        attendance_code_obj = AttendanceCode.objects.select_related('class_session__course').get(code=code)
        class_session = attendance_code_obj.class_session
    except AttendanceCode.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid attendance code.'}, status=400)

    if not attendance_code_obj.is_valid():
        return JsonResponse({'status': 'error', 'message': 'Attendance code has expired.'}, status=400)

    # Check if student is enrolled in the course associated with this class session
    # Using 'course_enrollments' here to filter enrollments from the course perspective,
    # ensuring the student is part of an enrollment for this specific course.
    if not class_session.course.course_enrollments.filter(student=request.user).exists():
        return JsonResponse({'status': 'error', 'message': 'You are not enrolled in this course.'}, status=403)

    # Prevent duplicate submissions for the same session by the same student
    if AttendanceRecord.objects.filter(class_session=class_session, student=request.user).exists():
        return JsonResponse({'status': 'info', 'message': 'You have already submitted attendance for this class.'}, status=200)

    # Simulate IP and Geolocation data from the client-side JavaScript
    simulated_ip = request.POST.get('simulated_ip')
    simulated_lat_str = request.POST.get('simulated_latitude')
    simulated_lon_str = request.POST.get('simulated_longitude')

    simulated_geolocation = None
    if simulated_lat_str and simulated_lon_str:
        try:
            # Ensure float conversion and handle potential errors
            simulated_geolocation = {
                'latitude': float(simulated_lat_str),
                'longitude': float(simulated_lon_str),
            }
        except ValueError:
            # If conversion fails, log and proceed with None for geolocation
            print(f"Invalid geolocation data: lat={simulated_lat_str}, lon={simulated_lon_str}")
            pass

    # Create the attendance record
    attendance_record = AttendanceRecord.objects.create(
        class_session=class_session,
        student=request.user,
        is_present=False, # Initially False, teacher explicitly validates
        simulated_ip=simulated_ip,
        simulated_geolocation=simulated_geolocation, # This should be directly saved if JSONField
    )

    # Send real-time notification to the relevant teachers (those teaching this class session)
    teacher_group_name = f'class_session_{class_session.id}_notifications'
    send_group_notification(
        group_name=teacher_group_name,
        message_type='student_submitted', # Specific message type for frontend
        message=f"Student {request.user.username} has submitted attendance for {class_session.course.name} on {class_session.date.strftime('%Y-%m-%d')}.",
        context={
            'id': str(attendance_record.id), # Frontend renderSubmissionRow needs 'id'
            'name': request.user.get_full_name() or request.user.username,
            'timestamp': attendance_record.timestamp.isoformat(), # Pass ISO format for JS Date parsing
            'simulatedIp': simulated_ip,
            'simulatedGeolocation': simulated_geolocation,
            'aiResult': None, # No AI result initially
            'is_present': attendance_record.is_present,
            'class_session_id': str(class_session.id), # For buttons in JS
        }
    )

    return JsonResponse({'status': 'success', 'message': 'Código de presença enviado com sucesso. Aguarda validação do professor.'})