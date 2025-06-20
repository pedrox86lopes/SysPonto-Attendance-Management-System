# attendance/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Main dashboard (routes based on user role)
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Teacher URLs
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/portal/', views.teacher_portal, name='teacher_portal'),
    path('teacher/generate-code/', views.teacher_generate_code, name='teacher_generate_code'),  # Legacy
    path('teacher/generate-code-page/', views.teacher_generate_code_page, name='teacher_generate_code_page'),  # Legacy
    
    # Student URLs
    path('student/dashboard/', views.student_dashboard_unified, name='student_dashboard'),
    path('student/portal/', views.student_portal, name='student_portal'),
    path('student/calendar/', views.student_calendar, name='student_calendar'),
    path('student/enter-code/', views.student_enter_code, name='student_enter_code'),
    # Justify absence page
    path('student/justify/', views.student_justify_absence, name='student_justify_absence'),

    
    # API Endpoints - Teacher
    path('api/generate-code/', views.generate_code_api_view, name='generate_code_api_view'),
    path('api/run-ai-validation/', views.run_ai_validation, name='run_ai_validation'),
    path('api/validate-attendance/', views.validate_attendance, name='validate_attendance'),
    path('api/get-session-submissions/', views.get_session_submissions, name='get_session_submissions'),
    
    # API Endpoints - Student
    path('api/submit-attendance/', views.submit_attendance_code, name='submit_attendance_code'),
    path('api/student/current-classes/', views.api_student_current_classes, name='api_student_current_classes'),
    path('api/student/today-classes/', views.api_student_today_classes, name='api_student_today_classes'),
    path('api/student/weekly-classes/', views.api_student_weekly_classes, name='api_student_weekly_classes'),
    path('api/student/attendance-history/', views.api_student_attendance_history, name='api_student_attendance_history'),
    path('api/submit-justification/', views.submit_justification, name='submit_justification'),

    
    # Home page
    path('', views.home, name='home'),
]