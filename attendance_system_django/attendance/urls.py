# attendance/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # New Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # New Student Dashboard
    path('student/dashboard/', views.student_dashboard_unified, name='student_dashboard_unified'),

    
    # Teacher Views
    path('teacher/', views.teacher_portal, name='teacher_portal'),
    path('teacher/generate-code/', views.teacher_generate_code, name='teacher_generate_code'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    # Remove duplicate line:
    # path('teacher/dashboard/', views.teacher_generate_code_page, name='teacher_dashboard'),

    # API Endpoints (consistent 'api/' prefix for all)
    path('api/generate-attendance-code/', views.generate_attendance_code, name='generate_attendance_code'),
    path('api/run-ai-validation/', views.run_ai_validation, name='run_ai_validation'),
    path('api/validate-attendance/', views.validate_attendance, name='validate_attendance'),
    path('api/get-session-submissions/', views.get_session_submissions, name='get_session_submissions'),
    # URL for the AJAX POST request to generate code
    path('api/generate-code/', views.generate_code_api_view, name='generate_code_api_view'),
    
    # Student API endpoints 
    path('api/student/current-classes/', views.api_student_current_classes, name='api_student_current_classes'),
    path('api/student/today-classes/', views.api_student_today_classes, name='api_student_today_classes'),
    path('api/student/weekly-classes/', views.api_student_weekly_classes, name='api_student_weekly_classes'),
    path('api/student/attendance-history/', views.api_student_attendance_history, name='api_student_attendance_history'),

    # Student Views
    path('student/', views.student_portal, name='student_portal'),
    path('student/enter-code/', views.student_enter_code, name='student_enter_code'),
    path('student/calendar/', views.student_calendar, name='student_calendar'),
    path('api/submit-attendance/', views.submit_attendance_code, name='submit_attendance_code'),
 
    # Logout URL 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]