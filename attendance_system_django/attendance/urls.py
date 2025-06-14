# attendance/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Import Django's default auth views

urlpatterns = [
    # Teacher URLs
    path('teacher/', views.teacher_portal, name='teacher_portal'),
    path('teacher/generate-code/', views.teacher_generate_code, name='teacher_generate_code'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/api/generate_code/', views.generate_attendance_code, name='generate_attendance_code'), # AJAX endpoint
    path('teacher/api/run_ai_validation/', views.run_ai_validation, name='run_ai_validation'), # AJAX endpoint
    path('teacher/api/validate_attendance/', views.validate_attendance, name='validate_attendance'), # AJAX endpoint

    # Student URLs (placeholder, will be detailed next)
    path('student/', views.student_portal, name='student_portal'),
    path('student/enter-code/', views.student_enter_code, name='student_enter_code'),
    path('student/calendar/', views.student_calendar, name='student_calendar'),
    path('student/api/submit_attendance/', views.submit_attendance_code, name='submit_attendance_code'), # AJAX endpoint
]