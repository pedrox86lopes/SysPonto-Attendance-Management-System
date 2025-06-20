# attendance/models.py

from django.db import models
from core.models import User
from courses.models import ClassSession, Course
from django.utils import timezone
import uuid
from datetime import timedelta


class AttendanceCode(models.Model):
    class_session = models.OneToOneField(ClassSession, on_delete=models.CASCADE, related_name='attendance_code')
    code = models.CharField(max_length=6, unique=True, blank=True) # Added blank=True if you set code in save()
    expires_at = models.DateTimeField(default=None, null=True) # Set a default in save() if not provided during creation
    created_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # <-- ADD THIS LINE
    is_active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if not self.code:
            import secrets
            import string
            characters = string.ascii_uppercase + string.digits
            self.code = ''.join(secrets.choice(characters) for _ in range(6))
        if not self.expires_at:
            # You might want to remove this default if you explicitly set expires_at in views.py
            # If you want this to be the fallback, keep it.
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_valid(self):
        return self.expires_at is not None and timezone.now() < self.expires_at

    def __str__(self):
        return f"Code: {self.code} for {self.class_session.course.name} ({'Valid' if self.is_valid() else 'Expired'})"

class AttendanceRecord(models.Model):
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_present = models.BooleanField(default=False)
    simulated_ip = models.GenericIPAddressField(null=True, blank=True)
    simulated_geolocation = models.JSONField(null=True, blank=True)
    ai_result = models.JSONField(null=True, blank=True) # Stores {"isFraudulent": bool, "fraudExplanation": str}

    class Meta:
        unique_together = ('class_session', 'student') # A student can only have one record per session
        ordering = ['-timestamp'] # Order by most recent first

    def __str__(self):
        status = "Present" if self.is_present else "Pending/Absent"
        return f"{self.student.username} - {self.class_session.course.name} on {self.class_session.date} ({status})"

class Enrollment(models.Model):
    # Renamed related_name to avoid conflicts and improve clarity
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course') # A student can enroll in a course only once

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.name}"
    
    # Justify Page
class AbsenceJustification(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='justifications')
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='justifications')
    description = models.TextField(max_length=500)
    document = models.FileField(upload_to='justifications/%Y/%m/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    justification_type = models.CharField(max_length=20, choices=[
        ('absence', 'Ausência Total'),
        ('late_arrival', 'Chegada Tardia'),
    ], default='absence')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ], default='pending')
    teacher_comment = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_justifications')

    class Meta:
        unique_together = ('student', 'class_session')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.username} - {self.class_session.course.name} ({self.status})"
