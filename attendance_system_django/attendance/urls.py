# attendance/urls.py
from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views # This line is not needed here if auth views are in main urls.py
# from django.urls import path, include # This line is duplicated, `path` is already imported

urlpatterns = [
	# Teacher Views
	path('teacher/', views.teacher_portal, name='teacher_portal'),
	path('teacher/generate-code/', views.teacher_generate_code, name='teacher_generate_code'),
	path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),


	# API Endpoints (consistent 'api/' prefix for all)
	path('api/generate-attendance-code/', views.generate_attendance_code, name='generate_attendance_code'), # Keep this one
	path('api/run-ai-validation/', views.run_ai_validation, name='run_ai_validation'),
	path('api/validate-attendance/', views.validate_attendance, name='validate_attendance'),
	path('api/get-session-submissions/', views.get_session_submissions, name='get_session_submissions'),

	# Student Views
	path('student/', views.student_portal, name='student_portal'),
	path('student/enter-code/', views.student_enter_code, name='student_enter_code'),
	path('student/calendar/', views.student_calendar, name='student_calendar'),
	path('api/submit-attendance/', views.submit_attendance_code, name='submit_attendance_code'),
 ]



    
