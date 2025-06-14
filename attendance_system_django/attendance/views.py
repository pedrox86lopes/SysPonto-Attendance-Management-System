# attendance/views.py

import json
import random # For simulating AI validation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
from django.urls import reverse

# Import your models
from core.models import User
from courses.models import Course, ClassSession
from attendance.models import AttendanceCode, AttendanceRecord, Enrollment

# Helper function to send notification to a group (from previous detailed response)
def send_group_notification(group_name, message_type, message, context={}):
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification', # This maps to the consumer's method name
                'message': message,
                'context': context,
            }
        )

# --- Role-based access decorators ---
def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'

def is_student(user):
    return user.is_authenticated and user.role == 'student'

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# --- Teacher Views ---

@login_required
@user_passes_test(is_teacher, login_url='/login/')
def teacher_portal(request):
    # This is the /teacher landing page (teacher/page.tsx equivalent)
    return render(request, 'teacher/teacher_portal.html')

@login_required
@user_passes_test(is_teacher, login_url='/login/')
def teacher_generate_code(request):
    # This corresponds to teacher/generate-code/page.tsx
    # We fetch the current active code for the teacher's *current* classes
    # For simplicity, we'll look for an active code in one of the teacher's active classes today.
    # In a real system, a teacher might select a specific class session to generate a code for.
    # We'll pass the *most recent* active code if any, or nothing.

    today = timezone.localdate()
    current_code_details = None

    # Find a class session taught by this teacher for today
    class_sessions_today = ClassSession.objects.filter(
        course__teachers=request.user,
        date=today
    ).order_by('-start_time') # Get the most recent one for default display

    for session in class_sessions_today:
        try:
            code_obj = AttendanceCode.objects.get(class_session=session)
            if code_obj.is_valid():
                current_code_details = {
                    'code': code_obj.code,
                    'class_session_id': session.id,
                    'expires_at': code_obj.expires_at.isoformat(),
                    'code_status': 'active' # Set on backend to simplify client-side status
                }
                break # Found an active code, use it
            else:
                # Code expired, but might still be returned if no active code found
                if current_code_details is None: # Only if no valid code was found yet
                     current_code_details = {
                        'code': code_obj.code,
                        'class_session_id': session.id,
                        'expires_at': code_obj.expires_at.isoformat(),
                        'code_status': 'expired'
                    }
        except AttendanceCode.DoesNotExist:
            pass # No code for this session

    if not current_code_details:
        current_code_details = {
            'code_status': 'inactive' # No code found or all expired
        }

    return render(request, 'teacher/teacher_generate_code.html', {
        'initial_code_details': json.dumps(current_code_details) # Pass as JSON string
    })


@login_required
@user_passes_test(is_teacher, login_url='/login/')
@require_POST
def generate_attendance_code(request):
    # This corresponds to the generateNewCode function from useAttendance
    # We'll assume the teacher is generating a code for an *active* class session they teach today.
    # In a real app, you might want a dropdown to select the class session.
    # For now, we'll pick the first available active class session for the teacher.

    teacher_classes_today = ClassSession.objects.filter(
        course__teachers=request.user,
        date=timezone.localdate()
    ).order_by('start_time')

    if not teacher_classes_today.exists():
        return JsonResponse({'status': 'error', 'message': 'You have no active classes today to generate a code for.'}, status=400)

    # Let's target the *first* class session that is either ongoing or upcoming today
    target_class_session = None
    now = timezone.now().time()
    for session in teacher_classes_today:
        if session.end_time > now: # Class has not ended yet
            target_class_session = session
            break

    if not target_class_session:
        return JsonResponse({'status': 'error', 'message': 'No upcoming or active class sessions found for today.'}, status=400)

    # Delete any existing code for this specific session
    AttendanceCode.objects.filter(class_session=target_class_session).delete()

    # Create a new code
    new_code_obj = AttendanceCode.objects.create(class_session=target_class_session)

    # Send notification to the teacher who generated it (and potentially their dashboard)
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


@login_required
@user_passes_test(is_student, login_url='/login/')
def student_portal(request):
    # This is the /student landing page
    return render(request, 'student/student_portal.html')

@login_required
@user_passes_test(is_student, login_url='/login/')
def student_enter_code(request):
    # This corresponds to /student/enter-code
    return render(request, 'student/student_enter_code.html')

@login_required
@user_passes_test(is_student, login_url='/login/')
def student_calendar(request):
    # This corresponds to /student/calendar
    # Fetch enrolled classes for the student
    enrolled_class_sessions = ClassSession.objects.filter(
        course__enrollment__student=request.user,
        date__gte=timezone.localdate() # Show upcoming classes
    ).order_by('date', 'start_time').select_related('course')

    # Format for FullCalendar.js (example)
    calendar_events = []
    for session in enrolled_class_sessions:
        calendar_events.append({
            'title': session.course.name,
            'start': f"{session.date.isoformat()}T{session.start_time.isoformat()}",
            'end': f"{session.date.isoformat()}T{session.end_time.isoformat()}",
            'id': session.id,
            # Add more data if needed, e.g., session details for a popup
        })

    return render(request, 'student/student_calendar.html', {
        'calendar_events_json': json.dumps(calendar_events)
    })

@login_required
@user_passes_test(is_student, login_url='/login/')
@require_POST
def submit_attendance_code(request):
    # This corresponds to student entering code
    code = request.POST.get('attendance_code')
    class_session_id = request.POST.get('class_session_id') # Will be optional/derived for simplicity

    if not code:
        return JsonResponse({'status': 'error', 'message': 'Attendance code is required.'}, status=400)

    try:
        attendance_code_obj = AttendanceCode.objects.select_related('class_session__course').get(code=code)
        class_session = attendance_code_obj.class_session
    except AttendanceCode.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid attendance code.'}, status=400)

    if not attendance_code_obj.is_valid():
        return JsonResponse({'status': 'error', 'message': 'Attendance code has expired.'}, status=400)

    # Check if student is enrolled in this class's course
    if not Enrollment.objects.filter(student=request.user, course=class_session.course).exists():
        return JsonResponse({'status': 'error', 'message': 'You are not enrolled in this course.'}, status=403)

    # Check if student already submitted for this session
    if AttendanceRecord.objects.filter(class_session=class_session, student=request.user).exists():
        return JsonResponse({'status': 'info', 'message': 'You have already submitted attendance for this class.'}, status=200)

    # Simulate IP and Geolocation (from client-side JavaScript, if available)
    simulated_ip = request.POST.get('simulated_ip', '192.168.1.1') # Placeholder
    simulated_lat = request.POST.get('simulated_latitude')
    simulated_lon = request.POST.get('simulated_longitude')

    simulated_geolocation = None
    if simulated_lat and simulated_lon:
        try:
            simulated_geolocation = {
                'latitude': float(simulated_lat),
                'longitude': float(simulated_lon),
            }
        except ValueError:
            pass # Invalid floats, keep as None

    attendance_record = AttendanceRecord.objects.create(
        class_session=class_session,
        student=request.user,
        is_present=False, # Initially False, teacher validates
        simulated_ip=simulated_ip,
        simulated_geolocation=simulated_geolocation,
    )

    # Send Notification to Teacher
    teacher_group_name = f'class_session_{class_session.id}_notifications'
    send_group_notification(
        group_name=teacher_group_name,
        message_type='student_submitted',
        message=f"Student {request.user.username} has submitted attendance for {class_session.course.name} on {class_session.date}.",
        context={
            'student_id': request.user.id,
            'student_name': request.user.username,
            'class_session_id': class_session.id,
            'attendance_record_id': attendance_record.id,
            'timestamp': attendance_record.timestamp.isoformat(),
            'simulated_ip': simulated_ip,
            'simulated_geolocation': simulated_geolocation,
        }
    )

    return JsonResponse({'status': 'success', 'message': 'Attendance code submitted successfully. Awaiting teacher validation.'})
