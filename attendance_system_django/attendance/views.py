# attendance/views.py
import os
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
from django.db.models import Count, Avg, Q, Case, When, IntegerField
from django.utils.timezone import localdate
import logging
import string
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from core.models import User
from courses.models import Course, ClassSession
from attendance.models import AttendanceCode, AttendanceRecord, Enrollment, AbsenceJustification


# Import your models
from core.models import User
from courses.models import Course, ClassSession

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Helper function to send notification to a group
def send_group_notification(group_name, message_type, message, context={}):
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': message_type,
                'message': message,
                'context': context,
            }
        )
        
# --- Role-based access decorators --- (Ensure these are in your views.py)
def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'

def is_student(user):
    return user.is_authenticated and user.role == 'student'

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# --- Get Code for Session ---
@login_required(login_url='/login/')
@user_passes_test(is_teacher, login_url='/login/')
@require_GET
def get_code_for_session(request):
    """
    API endpoint to get the current attendance code for a specific session.
    """
    class_session_id = request.GET.get('class_session_id')
    if not class_session_id:
        return JsonResponse({'status': 'error', 'message': 'Class session ID is required.'}, status=400)

    try:
        class_session = ClassSession.objects.get(id=class_session_id)
        # Verify the teacher is associated with this class's course
        if not class_session.course.teachers.filter(id=request.user.id).exists():
            return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)

        # Try to get the attendance code for this session
        try:
            attendance_code = AttendanceCode.objects.get(class_session=class_session)
            if attendance_code.is_valid():
                return JsonResponse({
                    'status': 'success',
                    'code_details': {
                        'code': attendance_code.code,
                        'expires_at': attendance_code.expires_at.isoformat(),
                        'is_valid': True
                    }
                })
            else:
                return JsonResponse({
                    'status': 'success',
                    'code_details': {
                        'code': attendance_code.code,
                        'expires_at': attendance_code.expires_at.isoformat(),
                        'is_valid': False
                    }
                })
        except AttendanceCode.DoesNotExist:
            return JsonResponse({
                'status': 'success',
                'code_details': None,
                'message': 'No code found for this session.'
            })

    except ClassSession.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Class session not found.'}, status=404)


# --- Consolidated Dashboard View ---
@login_required(login_url='/login/')
def dashboard_view(request): # You might map this to your '/' or '/dashboard/' URL
    context = {}
    
    # Common known valid locations (e.g., CESAE Digital)
    known_valid_locations = [{"latitude": 41.5431, "longitude": -8.4079}]
    context['known_valid_locations_json'] = json.dumps(known_valid_locations)

    if request.user.role == 'teacher':
        today = localdate()
        now_time = timezone.now().time()

        teacher_class_sessions_today = ClassSession.objects.filter(
            # Show ongoing/upcoming classes for today
            Q(start_time__lte=now_time, end_time__gte=now_time) | Q(start_time__gt=now_time),
            course__teachers=request.user,
            date=today
        ).order_by('start_time').select_related('course')

        current_code_details = {'code_status': 'inactive', 'code': None, 'class_session_id': None, 'expires_at': None}
        student_submissions_data = []
        active_class_session_for_display = None

        # Try to find an active code for today's sessions first
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
                    break # Found an active code, break loop
            except AttendanceCode.DoesNotExist:
                pass

        # If no active code found, but there are sessions, default to the first
        if not active_class_session_for_display and teacher_class_sessions_today.exists():
            active_class_session_for_display = teacher_class_sessions_today.first()
            try: # Check if there's an expired code for the default session
                expired_code_obj = AttendanceCode.objects.get(class_session=active_class_session_for_display)
                current_code_details = {
                    'code': expired_code_obj.code,
                    'class_session_id': str(expired_code_obj.class_session.id),
                    'expires_at': expired_code_obj.expires_at.isoformat(),
                    'code_status': 'expired'
                }
            except AttendanceCode.DoesNotExist:
                # No code at all for the default session
                current_code_details = {
                    'code_status': 'inactive',
                    'code': None,
                    'class_session_id': str(active_class_session_for_display.id),
                    'expires_at': None
                }
        
        # Fetch initial submissions for the active session (if any)
        if active_class_session_for_display:
            submissions = AttendanceRecord.objects.filter(
                class_session=active_class_session_for_display
            ).select_related('student').order_by('timestamp')
            
            for sub in submissions:
                ai_result_data = sub.ai_result # JSONField returns dict directly
                student_submissions_data.append({
                    'id': str(sub.id),
                    'name': sub.student.get_full_name() or sub.student.username,
                    'timestamp': sub.timestamp.isoformat(),
                    'simulatedIp': sub.simulated_ip,
                    'simulatedGeolocation': sub.simulated_geolocation,
                    'aiResult': ai_result_data,
                    'is_present': sub.is_present,
                    'class_session_id': str(active_class_session_for_display.id), # Add this for JS reference
                })

        context.update({
            'is_teacher_role': True, # Flag for template to show teacher content
            'teacher_class_sessions_today': teacher_class_sessions_today,
            'active_class_session_for_display': active_class_session_for_display,
            'initial_code_details_json': json.dumps(current_code_details), # Renamed for clarity
            'initial_student_submissions_json': json.dumps(student_submissions_data), # Renamed for clarity
            'active_class_session_id_initial': str(active_class_session_for_display.id) if active_class_session_for_display else 'null',
        })

    elif request.user.role == 'student':
        today = localdate()
        now_local_time = timezone.localtime().time()

        enrolled_courses_qs = Course.objects.filter(course_enrollments__student=request.user).distinct()
        today_sessions = ClassSession.objects.filter(
            course__course_enrollments__student=request.user,
            date=today,
        ).order_by('start_time').select_related('course')
        next_upcoming_session = ClassSession.objects.filter(
            course__course_enrollments__student=request.user
        ).filter(
            Q(date=today, start_time__gt=now_local_time) | Q(date__gt=today)
        ).order_by('date', 'start_time').select_related('course').first()

        student_history_records = AttendanceRecord.objects.filter(
            student=request.user
        ).order_by('-timestamp').select_related('class_session__course')

        history_data = []
        for record in student_history_records:
            history_data.append({
                'id': str(record.id),
                'course_name': record.class_session.course.name,
                'session_date': record.class_session.date.isoformat(),
                'status': 'Present' if record.is_present else 'Pending/Absent',
                'timestamp': record.timestamp.isoformat(),
            })

        context.update({
            'is_student_role': True, # Flag for template to show student content
            'enrolled_courses': enrolled_courses_qs,
            'today_sessions': today_sessions,
            'next_upcoming_session': next_upcoming_session,
            'student_history_json': json.dumps(history_data),
        })
    else:
        # Handle cases for other roles or unauthenticated users (e.g., redirect to login)
        pass 

    return render(request, 'dashboard.html', context) 


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

# --- Teacher Views / Analytics View ---
@login_required(login_url='/login/')
@user_passes_test(is_teacher, login_url='/login/')
def teacher_analytics(request):
    """
    Renders the detailed analytics page for teachers with comprehensive statistics.
    ALL DATA COMES FROM REAL DATABASE - NO SIMULATION
    """
    # Get time period from request (default to 30 days)
    period_days = int(request.GET.get('period', 30))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=period_days)
    
    # Get teacher's courses
    teacher_courses = Course.objects.filter(teachers=request.user)
    
    # Get class sessions in the period
    class_sessions = ClassSession.objects.filter(
        course__in=teacher_courses,
        date__range=[start_date, end_date]
    ).select_related('course')
    
    # Get attendance records
    attendance_records = AttendanceRecord.objects.filter(
        class_session__in=class_sessions
    ).select_related('student', 'class_session__course')
    
    # === DATABASE CALCULATIONS ===
    
    # Global statistics
    total_students = User.objects.filter(
        role='student',
        student_enrollments__course__in=teacher_courses
    ).distinct().count()
    
    total_classes = class_sessions.count()
    total_codes = AttendanceCode.objects.filter(class_session__in=class_sessions).count()
    
    # Calculate attendance rate
    total_submissions = attendance_records.count()
    present_submissions = attendance_records.filter(is_present=True).count()
    global_attendance_rate = round((present_submissions / total_submissions * 100), 1) if total_submissions > 0 else 0
    
    # === WEEKLY ATTENDANCE TREND ===
    weekly_trend = []
    weekly_labels = []
    
    for i in range(7, -1, -1):  # Last 8 weeks
        week_start = end_date - timedelta(days=end_date.weekday() + 7*i)
        week_end = week_start + timedelta(days=6)
        
        week_sessions = class_sessions.filter(date__range=[week_start, week_end])
        week_records = attendance_records.filter(class_session__in=week_sessions)
        week_present = week_records.filter(is_present=True).count()
        week_total = week_records.count()
        
        week_rate = round((week_present / week_total * 100), 1) if week_total > 0 else 0
        weekly_trend.append(week_rate)
        weekly_labels.append(f'Sem {8-i}')
    
    # === COURSE PERFORMANCE  ===
    course_performance = []
    course_labels = []
    
    for course in teacher_courses:
        course_sessions = class_sessions.filter(course=course)
        course_records = attendance_records.filter(class_session__in=course_sessions)
        course_present = course_records.filter(is_present=True).count()
        course_total = course_records.count()
        
        course_rate = round((course_present / course_total * 100), 1) if course_total > 0 else 0
        course_performance.append(course_rate)
        course_labels.append(course.name[:25])  # Truncate for display
    
    # === WEEKLY DISTRIBUTION BY DAY ===
    weekly_distribution = []
    weekly_dist_labels = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    
    # Django week_day: 1=Sunday, 2=Monday, ..., 6=Friday, 7=Saturday
    for day_num in range(2, 7):  # Monday=2 to Friday=6
        day_sessions = class_sessions.filter(date__week_day=day_num)
        day_records = attendance_records.filter(class_session__in=day_sessions)
        day_present = day_records.filter(is_present=True).count()
        day_total = day_records.count()
        
        day_rate = round((day_present / day_total * 100), 1) if day_total > 0 else 0
        weekly_distribution.append(day_rate)
    
    # === TIME DISTRIBUTION  ===
    # Count actual sessions by time periods
    morning_sessions = class_sessions.filter(start_time__lt='12:00').count()
    afternoon_sessions = class_sessions.filter(
        start_time__gte='12:00', 
        start_time__lt='18:00'
    ).count()
    evening_sessions = class_sessions.filter(start_time__gte='18:00').count()
    
    time_distribution = [morning_sessions, afternoon_sessions, evening_sessions]
    time_labels = ['Manhã (9h-12h)', 'Tarde (12h-18h)', 'Noite (18h+)']
    
    # === ATTENDANCE STATUS DISTRIBUTION ===
    present_count = attendance_records.filter(is_present=True).count()
    pending_count = attendance_records.filter(is_present=False).count()
    
    # Check if you have AbsenceJustification model for real justified absences
    try:
        from .models import AbsenceJustification
        justified_count = AbsenceJustification.objects.filter(
            class_session__in=class_sessions,
            status='approved'
        ).count()
        
        # Calculate late arrivals from justifications
        late_count = AbsenceJustification.objects.filter(
            class_session__in=class_sessions,
            justification_type='late_arrival'
        ).count()
        
        # Adjust pending count to exclude justified absences
        unjustified_count = max(0, pending_count - justified_count - late_count)
        
        attendance_status = [present_count, justified_count, unjustified_count, late_count]
        status_labels = ['Presente', 'Falta Justificada', 'Falta Injustificada', 'Chegada Tardia']
    except (ImportError, AttributeError):
        # Fallback if AbsenceJustification doesn't exist
        attendance_status = [present_count, pending_count]
        status_labels = ['Presente', 'Pendente/Ausente']
    
    # === TOP PERFORMING STUDENTS ===
    top_students = []
    
    # Get all students enrolled in teacher's courses
    enrolled_students = User.objects.filter(
        role='student',
        student_enrollments__course__in=teacher_courses
    ).distinct()
    
    for student in enrolled_students:
        student_records = attendance_records.filter(student=student)
        student_present = student_records.filter(is_present=True).count()
        student_total = student_records.count()
        
        if student_total > 0:  # Only include students with attendance records
            student_rate = round((student_present / student_total * 100), 1)
            top_students.append({
                'name': student.get_full_name() or student.username,
                'rate': student_rate,
                'classes': student_total
            })
    
    # Sort by rate and get top 10 (or all if less than 10)
    top_students = sorted(top_students, key=lambda x: x['rate'], reverse=True)[:10]
    
    # === COURSE STATISTICS ===
    course_stats = []
    
    for course in teacher_courses:
        # Count students enrolled in this specific course
        course_students = User.objects.filter(
            role='student',
            student_enrollments__course=course
        ).distinct().count()
        
        # Count sessions for this course in the period
        course_sessions_count = class_sessions.filter(course=course).count()
        
        # Get attendance records for this course
        course_records = attendance_records.filter(class_session__course=course)
        course_present = course_records.filter(is_present=True).count()
        course_total = course_records.count()
        
        # Calculate average attendance rate
        avg_rate = round((course_present / course_total * 100), 1) if course_total > 0 else 0
        
        course_stats.append({
            'name': course.name,
            'students': course_students,
            'avg_rate': avg_rate,
            'total_classes': course_sessions_count,
            'total_submissions': course_total,
            'present_submissions': course_present
        })
    
    # === PREVIOUS PERIOD COMPARISON (REAL DATA) ===
    prev_start_date = start_date - timedelta(days=period_days)
    prev_end_date = start_date
    
    prev_sessions = ClassSession.objects.filter(
        course__in=teacher_courses,
        date__range=[prev_start_date, prev_end_date]
    )
    prev_records = AttendanceRecord.objects.filter(class_session__in=prev_sessions)
    prev_present = prev_records.filter(is_present=True).count()
    prev_total = prev_records.count()
    prev_rate = round((prev_present / prev_total * 100), 1) if prev_total > 0 else 0
    
    rate_change = round(global_attendance_rate - prev_rate, 1)
    
    # === ADDITIONAL REAL METRICS ===
    
    # Code generation efficiency
    codes_per_session = round((total_codes / total_classes), 2) if total_classes > 0 else 0
    
    # Average students per class
    avg_students_per_class = round((total_submissions / total_classes), 1) if total_classes > 0 else 0
    
    # AI validation statistics (if ai_result field is used)
    ai_validated_records = attendance_records.exclude(ai_result__isnull=True).count()
    ai_flagged_records = attendance_records.filter(
        ai_result__icontains='"isFraudulent": true'
    ).count()
    
    # Calculate AI suspicion rate in the view instead of template
    ai_suspicion_rate = round((ai_flagged_records / ai_validated_records * 100), 1) if ai_validated_records > 0 else 0
    
    # === CONTEXT FOR TEMPLATE ===
    context = {
        # Global stats
        'global_attendance_rate': global_attendance_rate,
        'rate_change': rate_change,
        'total_students': total_students,
        'total_classes': total_classes,
        'total_codes': total_codes,
        'total_submissions': total_submissions,
        'present_submissions': present_submissions,
        'period_days': period_days,
        
        # Chart data (JSON serialized for JavaScript)
        'attendance_trend_data': json.dumps({
            'labels': weekly_labels,
            'data': weekly_trend
        }),
        'course_performance_data': json.dumps({
            'labels': course_labels,
            'data': course_performance
        }),
        'weekly_distribution_data': json.dumps({
            'labels': weekly_dist_labels,
            'data': weekly_distribution
        }),
        'time_distribution_data': json.dumps({
            'labels': time_labels,
            'data': time_distribution
        }),
        'attendance_status_data': json.dumps({
            'labels': status_labels,
            'data': attendance_status
        }),
        
        # Table data 
        'top_students': top_students,
        'course_stats': course_stats,
        
        # Additional metrics 
        'courses_count': teacher_courses.count(),
        'codes_per_session': codes_per_session,
        'avg_students_per_class': avg_students_per_class,
        'ai_validated_records': ai_validated_records,
        'ai_flagged_records': ai_flagged_records,
        'ai_suspicion_rate': ai_suspicion_rate,
        
        # Period information
        'start_date': start_date.strftime('%d/%m/%Y'),
        'end_date': end_date.strftime('%d/%m/%Y'),
        'prev_rate': prev_rate,
    }
    
    return render(request, 'teacher/teacher_analytics.html', context)

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
def teacher_generate_code_page(request): # Renamed for clarity, original name can stay if preferred
    """
    Renders the page for teachers to generate attendance codes.
    It pre-loads any currently active or recently expired code for the teacher's
    classes today.
    """
    today = timezone.localdate() # Use Django's timezone-aware localdate
    current_code_details = {'code_status': 'inactive', 'code': None, 'class_session_id': None, 'expires_at': None}

    # Ensure request.user is linked to a Teacher profile if your is_teacher decorator expects it
    # For example, if User has a OneToOneField to Teacher:
    # teacher_profile = request.user.teacher_profile # adjust as per your model setup

    class_sessions_today = ClassSession.objects.filter(
        course__teachers=request.user, # Assuming 'teachers' is a ManyToMany or ForeignKey on Course
        date=today
    ).order_by('start_time').select_related('course')

    active_class_session_for_display = None # To set the initial selected option in dropdown

    # Try to find an active code for today's sessions first
    for session in class_sessions_today:
        try:
            # Check if there's an active code for this specific session
            code_obj = AttendanceCode.objects.get(class_session=session)
            if code_obj.is_valid(): # Assumes you have an is_valid method on AttendanceCode
                current_code_details = {
                    'code': code_obj.code,
                    'class_session_id': str(session.id),
                    'expires_at': code_obj.expires_at.isoformat(),
                    'code_status': 'active'
                }
                active_class_session_for_display = session
                break # Found an active code, no need to check others
        except AttendanceCode.DoesNotExist:
            pass # No code for this specific session

    # If no active code was found, but there are sessions, default to the first session
    if not active_class_session_for_display and class_sessions_today.exists():
        active_class_session_for_display = class_sessions_today.first()
        current_code_details['class_session_id'] = str(active_class_session_for_display.id)
        # Note: current_code_details will still have code and expires_at as None unless set by an existing code

    # Calculate dashboard metrics
    total_students_enrolled = 0
    total_courses_taught = 0
    pending_validations = 0
    active_codes_count = 0
    
    # Get courses taught by this teacher
    teacher_courses = Course.objects.filter(teachers=request.user)
    total_courses_taught = teacher_courses.count()
    
    # Get total students enrolled in teacher's courses
    total_students_enrolled = User.objects.filter(
        role='student',
        student_enrollments__course__in=teacher_courses
    ).distinct().count()
    
    # Count pending validations (attendance records not marked as present)
    pending_validations = AttendanceRecord.objects.filter(
        class_session__course__teachers=request.user,
        is_present=False
    ).count()
    
    # Count active codes
    active_codes_count = AttendanceCode.objects.filter(
        class_session__course__teachers=request.user,
        expires_at__gt=timezone.now(),
        is_active=True
    ).count()

    # (You might need to fetch initial student submissions for the active session here as well)
    initial_student_submissions = [] # Populate this based on active_class_session_for_display if needed

    context = {
        'teacher_class_sessions_today': class_sessions_today,
        'initial_code_details': json.dumps(current_code_details),
        'active_class_session_for_display': active_class_session_for_display,
        'active_class_session_id': str(active_class_session_for_display.id) if active_class_session_for_display else '',
        'initial_student_submissions_parsed': initial_student_submissions, # Ensure this is properly formatted for JS
        # Dashboard metrics
        'total_students_enrolled': total_students_enrolled,
        'total_courses_taught': total_courses_taught,
        'current_day_sessions': class_sessions_today.count(), # Count of today's sessions
        'pending_validations': pending_validations,
        'active_codes_count': active_codes_count,  # Add this
        'total_present_attendance': 0, # Placeholder for chart
        'total_pending_attendance': 0, # Placeholder for chart
        'course_names_for_chart': json.dumps([]), # Placeholder for chart
        'submissions_per_course_for_chart': json.dumps([]), # Placeholder for chart
    }

    return render(request, 'teacher_dashboard.html', context)


# --- Generate Code API ---
@login_required
@user_passes_test(is_teacher)
@require_POST
def generate_code_api_view(request):
    """Handles the POST request to generate an attendance code"""
    class_session_id = request.POST.get('class_session_id')

    if not class_session_id:
        return JsonResponse({'status': 'error', 'message': 'ID da sessão de turma não fornecido.'}, status=400)

    try:
        class_session = get_object_or_404(ClassSession, id=class_session_id, course__teachers=request.user)
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'Sessão de turma não encontrada ou não pertence ao professor.'}, status=404)

    # Generate new code
    characters = string.ascii_uppercase + string.digits
    new_code = ''.join(random.choices(characters, k=6))
    expires_at = timezone.now() + timedelta(minutes=10)

    try:
        attendance_code, created = AttendanceCode.objects.update_or_create(
            class_session=class_session,
            defaults={
                'code': new_code,
                'expires_at': expires_at,
                'is_active': True,
                'generated_by': request.user,
            }
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Código gerado com sucesso!',
            'code': attendance_code.code,
            'expires_at': attendance_code.expires_at.isoformat(),
            'class_session_id': str(class_session.id)
        })

    except Exception as e:
        logger.error(f"Error saving attendance code: {e}")
        return JsonResponse({'status': 'error', 'message': f'Erro ao guardar código: {str(e)}'}, status=500)

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
    FIXED: Renders the teacher's attendance dashboard with proper metrics and code display.
    Fetches all ongoing/upcoming classes for the teacher today,
    and initial data for the most relevant class session.
    """
    today = localdate()
    now_time = timezone.now().time()

    # Get all today's sessions for the teacher
    teacher_class_sessions_today = ClassSession.objects.filter(
        course__teachers=request.user,
        date=today
    ).order_by('start_time').select_related('course')

    current_code_details = {'code_status': 'inactive', 'code': None, 'class_session_id': None, 'expires_at': None}
    student_submissions_data = []
    active_class_session_for_display = None

    # Try to find an active code for today's sessions first
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

    # If no active code found, but there are sessions, default to the first
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

    # Get submissions for the active session
    if active_class_session_for_display:
        submissions = AttendanceRecord.objects.filter(
            class_session=active_class_session_for_display
        ).select_related('student').order_by('timestamp')
        
        for sub in submissions:
            ai_result_data = sub.ai_result  # JSONField returns dict directly
            
            student_submissions_data.append({
                'id': str(sub.id),
                'name': sub.student.get_full_name() or sub.student.username,
                'timestamp': sub.timestamp.isoformat(),
                'simulatedIp': sub.simulated_ip,
                'simulatedGeolocation': sub.simulated_geolocation,
                'aiResult': ai_result_data,
                'is_present': sub.is_present,
                'class_session_id': str(active_class_session_for_display.id),
            })

    # FIXED: Calculate proper dashboard metrics
    teacher_courses = Course.objects.filter(teachers=request.user)
    
    # Total students enrolled in teacher's courses
    total_students_enrolled = User.objects.filter(
        role='student',
        student_enrollments__course__in=teacher_courses
    ).distinct().count()
    
    # Total courses taught
    total_courses_taught = teacher_courses.count()
    
    # Today's sessions count
    current_day_sessions = teacher_class_sessions_today.count()
    
    # Pending validations (attendance records not marked as present)
    pending_validations = AttendanceRecord.objects.filter(
        class_session__course__teachers=request.user,
        is_present=False
    ).count()
    
    # Active codes count
    active_codes_count = AttendanceCode.objects.filter(
        class_session__course__teachers=request.user,
        expires_at__gt=timezone.now(),
        is_active=True
    ).count()

    # Known valid locations (hardcoded for now, can come from model/settings in production)
    known_valid_locations = [
        {"latitude": 41.5369, "longitude": -8.4239}, # Example coordinates for CESAE Digital (Braga)
    ]

    context = {
        'teacher_class_sessions_today': teacher_class_sessions_today,
        'active_class_session_for_display': active_class_session_for_display,
        'initial_code_details': json.dumps(current_code_details),
        'initial_student_submissions': json.dumps(student_submissions_data),
        'active_class_session_id': str(active_class_session_for_display.id) if active_class_session_for_display else None,
        'total_students_enrolled': total_students_enrolled,
        'total_courses_taught': total_courses_taught,
        'current_day_sessions': current_day_sessions,
        'pending_validations': pending_validations,
        'active_codes_count': active_codes_count,
        # For the template compatibility
        'initial_code_details_json': json.dumps(current_code_details),
        'initial_student_submissions_json': json.dumps(student_submissions_data),
        'active_class_session_id_initial': str(active_class_session_for_display.id) if active_class_session_for_display else "",
    }
    return render(request, 'teacher/teacher_dashboard.html', context)


# --- AI Validation API ---
@login_required(login_url='/login/')
@user_passes_test(is_teacher, login_url='/login/')
@require_POST
def run_ai_validation(request):
    """API endpoint for teachers to trigger AI validation"""
    attendance_record_id = request.POST.get('attendance_record_id')
    class_session_id = request.POST.get('class_session_id')

    if not attendance_record_id or not class_session_id:
        return JsonResponse({'status': 'error', 'message': 'Record ID and Class Session ID are required.'}, status=400)

    try:
        record = AttendanceRecord.objects.get(id=attendance_record_id, class_session__id=class_session_id)
        if not record.class_session.course.teachers.filter(id=request.user.id).exists():
            return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)
    except AttendanceRecord.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Attendance record not found.'}, status=404)

    # Simulate AI Logic
    is_fraudulent = False
    fraud_explanation = "No issues detected."

    if random.random() < 0.2:  # 20% chance of fraud
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
        
        cesae_lat = 41.5431
        cesae_lon = -8.4079

        if sim_lat is not None and sim_lon is not None:
            lat_diff = abs(sim_lat - cesae_lat) * 111
            lon_diff = abs(sim_lon - cesae_lon) * 111 * abs(math.cos(math.radians(cesae_lat)))

            if lat_diff > 0.5 or lon_diff > 0.5:
                is_fraudulent = True
                fraud_explanation = "Geolocation is outside the expected classroom area."
        else:
            is_fraudulent = True
            fraud_explanation = "Incomplete geolocation data provided."
    else:
        is_fraudulent = True
        fraud_explanation = "Geolocation data missing or could not be obtained."

    ai_result_dict = {
        'isFraudulent': is_fraudulent,
        'fraudExplanation': fraud_explanation
    }
    record.ai_result = ai_result_dict
    record.save()

    return JsonResponse({
        'status': 'success',
        'aiResult': ai_result_dict,
        'attendance_record_id': str(record.id)
    })


# --- Validate Attendance API ---
@login_required(login_url='/login/')
@user_passes_test(is_teacher, login_url='/login/')
@require_POST
def validate_attendance(request):
    """API endpoint for teachers to validate attendance"""
    attendance_record_id = request.POST.get('attendance_record_id')
    if not attendance_record_id:
        return JsonResponse({'status': 'error', 'message': 'Attendance record ID is required.'}, status=400)

    try:
        attendance_record = AttendanceRecord.objects.get(id=attendance_record_id)
        if not attendance_record.class_session.course.teachers.filter(id=request.user.id).exists():
            return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)
    except AttendanceRecord.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Attendance record not found.'}, status=404)

    attendance_record.is_present = True
    attendance_record.save()

    return JsonResponse({'status': 'success', 'message': 'Attendance validated successfully.'})

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

    return JsonResponse({'status': 'success', 'message': 'Attendance validated successfully.'})
    
# --- Get Session Submissions API ---
@login_required(login_url='/login/')
@user_passes_test(is_teacher, login_url='/login/')
@require_GET
def get_session_submissions(request):
    """API endpoint to fetch attendance submissions for a specific class session"""
    class_session_id = request.GET.get('class_session_id')
    if not class_session_id:
        return JsonResponse({'status': 'error', 'message': 'Class session ID is required.'}, status=400)

    try:
        class_session = ClassSession.objects.get(id=class_session_id)
        if not class_session.course.teachers.filter(id=request.user.id).exists():
            return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)
    except ClassSession.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Class session not found.'}, status=404)

    submissions = AttendanceRecord.objects.filter(
        class_session=class_session
    ).select_related('student').order_by('timestamp')

    student_submissions_data = []
    for sub in submissions:
        student_submissions_data.append({
            'id': str(sub.id),
            'name': sub.student.get_full_name() or sub.student.username,
            'timestamp': sub.timestamp.isoformat(),
            'simulatedIp': sub.simulated_ip,
            'simulatedGeolocation': sub.simulated_geolocation,
            'aiResult': sub.ai_result,
            'is_present': sub.is_present,
            'class_session_id': str(class_session.id),
        })

    return JsonResponse({'status': 'success', 'submissions': student_submissions_data})

# --- Student / Justify Absence ---
@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
@require_POST
def submit_justification(request):
    """API endpoint for students to submit absence justification"""
    try:
        class_session_id = request.POST.get('class_session_id')
        description = request.POST.get('description', '').strip()
        is_late_arrival = request.POST.get('is_late_arrival', 'false').lower() == 'true'
        uploaded_file = request.FILES.get('document')

        if not class_session_id or not description:
            return JsonResponse({'status': 'error', 'message': 'Todos os campos são obrigatórios.'}, status=400)

        # Get and validate class session
        try:
            class_session = ClassSession.objects.get(id=class_session_id)
        except ClassSession.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Sessão de aula não encontrada.'}, status=404)

        # Check if student is enrolled in the course
        if not class_session.course.course_enrollments.filter(student=request.user).exists():
            return JsonResponse({'status': 'error', 'message': 'Não está inscrito neste curso.'}, status=403)

        # Validate timing based on justification type
        now = timezone.now()
        class_start = timezone.make_aware(datetime.combine(class_session.date, class_session.start_time))
        class_end = timezone.make_aware(datetime.combine(class_session.date, class_session.end_time))
        
        if is_late_arrival:
            # For late arrival: class must be currently running
            if not (class_start <= now <= class_end):
                return JsonResponse({'status': 'error', 'message': 'Esta aula não está a decorrer no momento.'}, status=400)
        else:
            # For absence: class must be in the past but within 30 days
            days_since_class = (now.date() - class_session.date).days
            if days_since_class < 0:
                return JsonResponse({'status': 'error', 'message': 'Não pode justificar aulas futuras.'}, status=400)
            if days_since_class > 30:
                return JsonResponse({'status': 'error', 'message': 'Prazo de justificação expirado (máximo 30 dias).'}, status=400)

        # For past classes (absence), file is required
        if not is_late_arrival and not uploaded_file:
            return JsonResponse({'status': 'error', 'message': 'Documento obrigatório para justificar ausências.'}, status=400)

        # Check for duplicate justification
        if AbsenceJustification.objects.filter(student=request.user, class_session=class_session).exists():
            return JsonResponse({'status': 'error', 'message': 'Já enviou uma justificação para esta aula.'}, status=400)

        # Validate file if provided
        if uploaded_file:
            # Check file size (5MB max)
            if uploaded_file.size > 5 * 1024 * 1024:
                return JsonResponse({'status': 'error', 'message': 'Ficheiro muito grande. Máximo 5MB.'}, status=400)
            
            # Check file type
            allowed_types = ['.pdf', '.png', '.jpg', '.jpeg', '.txt']
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            if file_extension not in allowed_types:
                return JsonResponse({'status': 'error', 'message': 'Tipo de ficheiro não suportado.'}, status=400)

        # Create the justification
        justification = AbsenceJustification.objects.create(
            student=request.user,
            class_session=class_session,
            description=description,
            document=uploaded_file,
            justification_type='late_arrival' if is_late_arrival else 'absence'  # Add this field to model
        )

        success_message = 'Justificação de chegada tardia enviada!' if is_late_arrival else 'Justificação de ausência enviada!'
        
        return JsonResponse({
            'status': 'success',
            'message': success_message,
            'justification_id': str(justification.id)
        })

    except Exception as e:
        logger.error(f"Error submitting justification: {e}")
        return JsonResponse({'status': 'error', 'message': 'Erro interno do servidor.'}, status=500)

# --- Student / Justify Absence ---
@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
def student_justify_absence(request):
    """Renders the student absence justification page."""
    today = timezone.now().date()
    
    # Get classes from past 60 days AND today (including current/future classes today)
    past_60_days = today - timedelta(days=60)
    tomorrow = today + timedelta(days=1)
    
    # Include past classes AND all of today's classes (past, current, and future)
    all_sessions = ClassSession.objects.filter(
        course__course_enrollments__student=request.user,
        date__range=[past_60_days, today]  # This includes today's classes
    ).select_related('course').order_by('-date', '-start_time')
    
    # Format for calendar events JSON
    calendar_events = []
    for session in all_sessions:
        start_datetime = timezone.make_aware(
            datetime.combine(session.date, session.start_time)
        )
        end_datetime = timezone.make_aware(
            datetime.combine(session.date, session.end_time)
        )
        
        calendar_events.append({
            'id': session.id,
            'title': session.course.name,
            'course_name': session.course.name,
            'start': start_datetime.isoformat(),
            'end': end_datetime.isoformat(),
        })
    
    # Get recent justifications (same as before)
    try:
        recent_justifications = AbsenceJustification.objects.filter(
            student=request.user
        ).select_related('class_session__course').order_by('-submitted_at')[:5]
        
        justifications_data = []
        for justification in recent_justifications:
            justifications_data.append({
                'id': str(justification.id),
                'course_name': justification.class_session.course.name,
                'class_date': justification.class_session.date.isoformat(),
                'status': justification.status,
                'submitted_at': justification.submitted_at.isoformat(),
                'description': justification.description[:100] + '...' if len(justification.description) > 100 else justification.description,
            })
    except:
        # If AbsenceJustification model doesn't exist yet
        justifications_data = []
    
    context = {
        'calendar_events_json': json.dumps(calendar_events),
        'recent_justifications_json': json.dumps(justifications_data),
    }
    
    return render(request, 'student/justify.html', context)

# --- Student Views ---

@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
@require_GET
def api_student_attendance_history(request):
    """API endpoint to get student's attendance history"""
    try:
        limit = int(request.GET.get('limit', 10))
        
        attendance_history = AttendanceRecord.objects.filter(
            student=request.user
        ).select_related('class_session__course').order_by('-timestamp')[:limit]
        
        history_data = [{
            'id': str(record.id),
            'course_name': record.class_session.course.name,
            'timestamp': record.timestamp.isoformat(),
            'is_present': record.is_present,
            'status': 'Present' if record.is_present else 'Pending',
            'session_date': record.class_session.date.isoformat()
        } for record in attendance_history]
        
        return JsonResponse({
            'status': 'success',
            'attendance_history': history_data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

# --- Student Dashboard ---
@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
def student_dashboard_unified(request):
    """
    FIXED: Student dashboard with proper data for student_portal.html template
    """
    # Get user's enrolled courses
    enrolled_courses = Course.objects.filter(
        course_enrollments__student=request.user
    ).distinct()
    
    # Get today's classes
    today = timezone.now().date()
    today_sessions = ClassSession.objects.filter(
        course__course_enrollments__student=request.user,
        date=today
    ).select_related('course').order_by('start_time')
    
    # Get this week's classes
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    weekly_sessions = ClassSession.objects.filter(
        course__course_enrollments__student=request.user,
        date__range=[week_start, week_end]
    ).select_related('course').order_by('date', 'start_time')
    
    # Get attendance history (last 10 records)
    attendance_history = AttendanceRecord.objects.filter(
        student=request.user
    ).select_related('class_session__course').order_by('-timestamp')[:10]
    
    # FIXED: Find current running classes
    now = timezone.now()
    current_time = now.time()
    current_sessions = ClassSession.objects.filter(
        course__course_enrollments__student=request.user,
        date=today,
        start_time__lte=current_time,
        end_time__gte=current_time
    ).select_related('course')
    
    # Prepare JSON data for frontend
    def format_session_for_json(session):
        start_datetime = timezone.make_aware(
            datetime.combine(session.date, session.start_time)
        )
        end_datetime = timezone.make_aware(
            datetime.combine(session.date, session.end_time)
        )
        
        return {
            'id': session.id,
            'title': session.course.name,
            'course_name': session.course.name,
            'start_datetime': start_datetime.isoformat(),
            'end_datetime': end_datetime.isoformat(),
            'start': start_datetime.isoformat(),
            'end': end_datetime.isoformat(),
        }
    
    today_classes_json = json.dumps([
        format_session_for_json(session) for session in today_sessions
    ])
    
    weekly_classes_json = json.dumps([
        format_session_for_json(session) for session in weekly_sessions
    ])
    
    attendance_history_json = json.dumps([{
        'id': str(record.id),
        'course_name': record.class_session.course.name,
        'timestamp': record.timestamp.isoformat(),
        'is_present': record.is_present,
        'status': 'Present' if record.is_present else 'Pending',
        'session_date': record.class_session.date.isoformat()
    } for record in attendance_history])
    
    current_classes_json = json.dumps([
        format_session_for_json(session) for session in current_sessions
    ])
    
    # Calendar events for compatibility
    calendar_events = []
    for session in weekly_sessions:
        calendar_events.append({
            'title': session.course.name,
            'start': f"{session.date.isoformat()}T{session.start_time.isoformat()}",
            'end': f"{session.date.isoformat()}T{session.end_time.isoformat()}",
            'id': session.id,
        })
    
    context = {
        'enrolled_courses': enrolled_courses,
        'today_sessions': today_sessions,
        'weekly_sessions': weekly_sessions,
        'attendance_history': attendance_history,
        'current_sessions': current_sessions,
        'today_classes_json': today_classes_json,
        'weekly_classes_json': weekly_classes_json,
        'attendance_history_json': attendance_history_json,
        'current_classes_json': current_classes_json,
        'calendar_events_json': json.dumps(calendar_events),
        # Counts for dashboard metrics
        'today_classes_count': today_sessions.count(),
        'weekly_classes_count': weekly_sessions.count(),
        'current_classes_count': current_sessions.count(),
    }
    
    return render(request, 'student/student_portal.html', context)

# API endpoints for student dashboard
@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
@require_GET
def api_student_current_classes(request):
    """API endpoint to get currently running classes for the student"""
    try:
        now = timezone.now()
        current_time = now.time()
        current_sessions = ClassSession.objects.filter(
            course__course_enrollments__student=request.user,
            date=now.date(),
            start_time__lte=current_time,
            end_time__gte=current_time
        ).select_related('course')
        
        current_classes = [{
            'id': session.id,
            'course_name': session.course.name,
            'start_datetime': timezone.make_aware(
                datetime.combine(session.date, session.start_time)
            ).isoformat(),
            'end_datetime': timezone.make_aware(
                datetime.combine(session.date, session.end_time)
            ).isoformat(),
        } for session in current_sessions]
        
        return JsonResponse({
            'status': 'success',
            'current_classes': current_classes
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
@require_GET
def api_student_today_classes(request):
    """API endpoint to get today's classes for the student"""
    try:
        today = timezone.now().date()
        today_sessions = ClassSession.objects.filter(
            course__course_enrollments__student=request.user,
            date=today
        ).select_related('course').order_by('start_time')
        
        today_classes = [{
            'id': session.id,
            'course_name': session.course.name,
            'start_datetime': timezone.make_aware(
                datetime.combine(session.date, session.start_time)
            ).isoformat(),
            'end_datetime': timezone.make_aware(
                datetime.combine(session.date, session.end_time)
            ).isoformat(),
        } for session in today_sessions]
        
        return JsonResponse({
            'status': 'success',
            'today_classes': today_classes
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
@require_GET
def api_student_weekly_classes(request):
    """API endpoint to get this week's classes for the student"""
    try:
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        weekly_sessions = ClassSession.objects.filter(
            course__course_enrollments__student=request.user,
            date__range=[week_start, week_end]
        ).select_related('course').order_by('date', 'start_time')
        
        weekly_classes = [{
            'id': session.id,
            'course_name': session.course.name,
            'start_datetime': timezone.make_aware(
                datetime.combine(session.date, session.start_time)
            ).isoformat(),
            'end_datetime': timezone.make_aware(
                datetime.combine(session.date, session.end_time)
            ).isoformat(),
        } for session in weekly_sessions]
        
        return JsonResponse({
            'status': 'success',
            'weekly_classes': weekly_classes
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

# Helper function to check if user is student
def is_student(user):
    """
    Check if the user has student role
    """
    return hasattr(user, 'role') and user.role == 'student'

# If you don't have this function already, add it
def is_teacher(user):
    """
    Check if the user has teacher role
    """
    return hasattr(user, 'role') and user.role == 'teacher'
    
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
    return student_dashboard_unified(request)

# Other views that might be referenced
@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
def student_enter_code(request):
    """Renders the page where students can enter attendance codes"""
    return render(request, 'student/student_enter_code.html')

# Student Calendar View
@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
@require_GET
def student_calendar(request):
    """Renders the student's calendar page"""
    enrolled_class_sessions = ClassSession.objects.filter(
        course__course_enrollments__student=request.user,
        date__gte=timezone.localdate()
    ).order_by('date', 'start_time').select_related('course')

    calendar_events = []
    for session in enrolled_class_sessions:
        calendar_events.append({
            'title': session.course.name,
            'start': f"{session.date.isoformat()}T{session.start_time.isoformat()}",
            'end': f"{session.date.isoformat()}T{session.end_time.isoformat()}",
            'id': session.id,
        })

    return render(request, 'student/student_calendar.html', {
        'calendar_events_json': json.dumps(calendar_events)
    })

# --- Submit Attendance API ---
@login_required(login_url='/login/')
@user_passes_test(is_student, login_url='/login/')
@require_POST
def submit_attendance_code(request):
    """API endpoint for students to submit an attendance code"""
    code = request.POST.get('attendance_code', '').strip().upper()

    if not code:
        return JsonResponse({'status': 'error', 'message': 'Attendance code is required.'}, status=400)

    try:
        attendance_code_obj = AttendanceCode.objects.select_related('class_session__course').get(code=code)
        class_session = attendance_code_obj.class_session
    except AttendanceCode.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Código de presença inválido.'}, status=400)

    if not attendance_code_obj.is_valid():
        return JsonResponse({'status': 'error', 'message': 'Código de presença expirado.'}, status=400)

    # Check if student is enrolled
    if not class_session.course.course_enrollments.filter(student=request.user).exists():
        return JsonResponse({'status': 'error', 'message': 'Não está inscrito neste curso.'}, status=403)

    # Prevent duplicate submissions
    if AttendanceRecord.objects.filter(class_session=class_session, student=request.user).exists():
        return JsonResponse({'status': 'info', 'message': 'Já enviou a presença para esta aula.'}, status=200)

    # Get simulated data
    simulated_ip = request.POST.get('simulated_ip')
    simulated_lat_str = request.POST.get('simulated_latitude')
    simulated_lon_str = request.POST.get('simulated_longitude')

    simulated_geolocation = None
    if simulated_lat_str and simulated_lon_str:
        try:
            simulated_geolocation = {
                'latitude': float(simulated_lat_str),
                'longitude': float(simulated_lon_str),
            }
        except ValueError:
            logger.warning(f"Invalid geolocation data: lat={simulated_lat_str}, lon={simulated_lon_str}")

    # Create attendance record
    attendance_record = AttendanceRecord.objects.create(
        class_session=class_session,
        student=request.user,
        is_present=False,  # Initially False, teacher validates
        simulated_ip=simulated_ip,
        simulated_geolocation=simulated_geolocation,
    )

    # Send real-time notification to teachers
    teacher_group_name = f'class_session_{class_session.id}_notifications'
    send_group_notification(
        group_name=teacher_group_name,
        message_type='student_submitted',
        message=f"Student {request.user.username} has submitted attendance for {class_session.course.name}.",
        context={
            'type': 'student_submitted',
            'id': str(attendance_record.id),
            'name': request.user.get_full_name() or request.user.username,
            'timestamp': attendance_record.timestamp.isoformat(),
            'simulatedIp': simulated_ip,
            'simulatedGeolocation': simulated_geolocation,
            'aiResult': None,
            'is_present': attendance_record.is_present,
            'class_session_id': str(class_session.id),
        }
    )

    return JsonResponse({'status': 'success', 'message': 'Código de presença enviado com sucesso. Aguarda validação do professor.'})

# Home page view
def home(request):
    """Home page that shows different content based on user role"""
    if request.user.is_authenticated:
        if request.user.role == 'teacher':
            return redirect('teacher_dashboard')
        elif request.user.role == 'student':
            return redirect('student_dashboard')
        else:
            return redirect('dashboard')
    else:
        return render(request, 'registration/login.html')