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
from datetime import datetime
from django.urls import reverse
from django.db.models import Q 

# Import your models
from core.models import User
from courses.models import Course, ClassSession
from attendance.models import AttendanceCode, AttendanceRecord, Enrollment


# Helper function to send notification to a group
def send_group_notification(group_name, message_type, message, context={}):
    """
    Sends a message to a specific Channel Layer group.
    This is used to send real-time notifications to connected WebSockets.
    """
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification', # This maps to the method in your consumer (e.g., NotificationConsumer.send_notification)
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
    today = timezone.localdate()
    current_code_details = None

    # Find a class session taught by this teacher for today
    # Ordering by -start_time to prioritize later classes if multiple exist
    class_sessions_today = ClassSession.objects.filter(
        course__teachers=request.user,
        date=today
    ).order_by('-start_time').select_related('course') # Eager load course to avoid extra queries

    for session in class_sessions_today:
        try:
            code_obj = AttendanceCode.objects.get(class_session=session)
            if code_obj.is_valid():
                # Found an active code, use it and stop searching
                current_code_details = {
                    'code': code_obj.code,
                    'class_session_id': session.id,
                    'expires_at': code_obj.expires_at.isoformat(),
                    'code_status': 'active'
                }
                break
            else:
                # Code expired. If no active code has been found yet,
                # store this expired one as the "current" one to display its status.
                if current_code_details is None or current_code_details['code_status'] != 'active':
                     current_code_details = {
                        'code': code_obj.code,
                        'class_session_id': session.id,
                        'expires_at': code_obj.expires_at.isoformat(),
                        'code_status': 'expired'
                    }
        except AttendanceCode.DoesNotExist:
            pass # No code for this session, continue to next session

    if not current_code_details:
        # If no codes (active or expired) were found for any classes today
        current_code_details = {
            'code_status': 'inactive',
            'code': None, # Explicitly set code to None
            'class_session_id': None,
            'expires_at': None,
        }

    return render(request, 'teacher/teacher_generate_code.html', {
        'initial_code_details': json.dumps(current_code_details) # Pass as JSON string for JS
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
        today = timezone.localdate()
        now_time = timezone.now().time()
        if target_class_session.date != today or target_class_session.end_time < now_time:
             return JsonResponse({'status': 'error', 'message': 'Cannot generate code for past or non-today class.'}, status=400)


    except ClassSession.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Class session not found.'}, status=404)

    # Delete any existing attendance code for this specific session
    AttendanceCode.objects.filter(class_session=target_class_session).delete()

    # Create a new attendance code for the target session
    # The 10-minute expiry is handled in the AttendanceCode model's save method.
    new_code_obj = AttendanceCode.objects.create(class_session=target_class_session)

    # Send a real-time notification to the teacher (their personal group)
    # This ensures the 'generate-code' page updates automatically if open.
    send_group_notification(
        group_name=f'teacher_{request.user.id}_general_notifications',
        message_type='code_generated_for_teacher',
        message=f"New code '{new_code_obj.code}' generated for {target_class_session.course.name}!",
        context={
            'code': new_code_obj.code,
            'class_session_id': target_class_session.id,
            'expires_at': new_code_obj.expires_at.isoformat(),
            'code_status': 'active'
        }
    )

    return JsonResponse({
        'status': 'success',
        'code': new_code_obj.code,
        'class_session_id': target_class_session.id,
        'expires_at': new_code_obj.expires_at.isoformat(),
    })


@login_required(login_url='/login/')
@user_passes_test(is_teacher, login_url='/login/')
def teacher_dashboard(request):
    """
    Renders the teacher's attendance dashboard.
    Fetches all ongoing/upcoming classes for the teacher today,
    and initial data for the most relevant class session.
    """
    today = timezone.localdate()
    now_time = timezone.now().time()

    # Get all active/upcoming class sessions for the current teacher today
    # These are the classes the teacher can select to generate codes for.
    teacher_class_sessions_today = ClassSession.objects.filter(
        course__teachers=request.user,
        date=today,
        end_time__gte=now_time # Only classes that are ongoing or start later today
    ).order_by('start_time').select_related('course')

    current_code_details = {'code_status': 'inactive', 'code': None, 'class_session_id': None, 'expires_at': None}
    student_submissions_data = []
    active_class_session_for_display = None # The session whose submissions are currently shown

    # Determine the "active" session for dashboard display (prioritize active code or next upcoming)
    for session in teacher_class_sessions_today:
        try:
            code_obj = AttendanceCode.objects.get(class_session=session)
            if code_obj.is_valid():
                active_class_session_for_display = session
                current_code_details = {
                    'code': code_obj.code,
                    'class_session_id': session.id,
                    'expires_at': code_obj.expires_at.isoformat(),
                    'code_status': 'active'
                }
                break # Found an active code, use this session for primary display
            elif not active_class_session_for_display: # If no active code yet, but this class is still relevant today
                active_class_session_for_display = session
                current_code_details = {
                    'code': code_obj.code,
                    'class_session_id': session.id,
                    'expires_at': code_obj.expires_at.isoformat(),
                    'code_status': 'expired'
                }
        except AttendanceCode.DoesNotExist:
            if not active_class_session_for_display: # If no code exists, but class is still relevant
                active_class_session_for_display = session

    # If no relevant class found with or without code, just pick the first one if any exist
    if not active_class_session_for_display and teacher_class_sessions_today.exists():
        active_class_session_for_display = teacher_class_sessions_today.first()
        current_code_details = {'code_status': 'inactive', 'code': None, 'class_session_id': active_class_session_for_display.id, 'expires_at': None}


    # Fetch student submissions for the determined active_class_session_for_display
    if active_class_session_for_display:
        submissions = AttendanceRecord.objects.filter(
            class_session=active_class_session_for_display
        ).select_related('student').order_by('timestamp') # Order by timestamp
        
        for sub in submissions:
            student_submissions_data.append({
                'id': sub.id,
                'name': sub.student.username,
                'timestamp': sub.timestamp.isoformat(),
                'simulatedIp': sub.simulated_ip,
                'simulatedGeolocation': sub.simulated_geolocation,
                'aiResult': sub.ai_result,
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
        'active_class_session_id': active_class_session_for_display.id if active_class_session_for_display else None
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
    if record.simulated_geolocation:
        sim_lat = record.simulated_geolocation.get('latitude')
        sim_lon = record.simulated_geolocation.get('longitude')
        
        # Define the primary valid location (e.g., CESAE Digital)
        cesae_lat = 41.5369
        cesae_lon = -8.4239
        
        # Simple distance check (using approximate degree-to-km conversion for small distances)
        # 1 degree lat is approx 111 km, 1 degree lon is approx 111*cos(lat) km
        # Added math.radians for correct cosine calculation
        lat_diff = abs(sim_lat - cesae_lat) * 111
        lon_diff = abs(sim_lon - cesae_lon) * 111 * abs(math.cos(math.radians(cesae_lat))) 

        if lat_diff > 0.5 or lon_diff > 0.5: # If distance is > 0.5 km
            is_fraudulent = True
            fraud_explanation = "Geolocation is outside the expected classroom area."
    else:
        # If no geolocation provided, consider it suspicious for AI check
        is_fraudulent = True
        fraud_explanation = "Geolocation data missing or could not be obtained."


    record.ai_result = {
        'isFraudulent': is_fraudulent,
        'fraudExplanation': fraud_explanation
    }
    record.save()

    return JsonResponse({
        'status': 'success',
        'aiResult': record.ai_result,
        'attendance_record_id': record.id
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

    # Send Notification to the specific Student whose attendance was validated
    student_group_name = f'user_{attendance_record.student.id}_notifications'
    send_group_notification(
        group_name=student_group_name,
        message_type='attendance_validated',
        message=f"Your attendance for {attendance_record.class_session.course.name} on {attendance_record.class_session.date.strftime('%Y-%m-%d')} has been validated!",
        context={
            'class_name': str(attendance_record.class_session),
            'status': 'present',
            'record_id': attendance_record.id,
            'class_session_id': attendance_record.class_session.id,
        }
    )

    return JsonResponse({'status': 'success', 'message': 'Attendance validated successfully.'})

# --- Student Views ---

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
        course__course_enrollments__student=request.user, # <--- Corrected this line
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
    simulated_lat = request.POST.get('simulated_latitude')
    simulated_lon = request.POST.get('simulated_longitude')

    simulated_geolocation = None
    if simulated_lat and simulated_lon:
        try:
            # Ensure float conversion and handle potential errors
            simulated_geolocation = {
                'latitude': float(simulated_lat),
                'longitude': float(simulated_lon),
            }
        except ValueError:
            # If conversion fails, log and proceed with None for geolocation
            print(f"Invalid geolocation data: lat={simulated_lat}, lon={simulated_lon}")
            pass

    # Create the attendance record
    attendance_record = AttendanceRecord.objects.create(
        class_session=class_session,
        student=request.user,
        is_present=False, # Initially False, teacher explicitly validates
        simulated_ip=simulated_ip,
        simulated_geolocation=simulated_geolocation,
    )

    # Send real-time notification to the relevant teachers (those teaching this class session)
    teacher_group_name = f'class_session_{class_session.id}_notifications'
    send_group_notification(
        group_name=teacher_group_name,
        message_type='student_submitted',
        message=f"Student {request.user.username} has submitted attendance for {class_session.course.name} on {class_session.date.strftime('%Y-%m-%d')}.",
        context={
            'student_id': request.user.id,
            'student_name': request.user.username,
            'class_session_id': class_session.id,
            'attendance_record_id': attendance_record.id,
            'timestamp': attendance_record.timestamp.isoformat(), # Pass ISO format for JS Date parsing
            'simulated_ip': simulated_ip,
            'simulated_geolocation': simulated_geolocation,
        }
    )

    return JsonResponse({'status': 'success', 'message': 'Attendance code submitted successfully. Awaiting teacher validation.'})