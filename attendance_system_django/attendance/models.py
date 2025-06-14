# attendance/models.py
import secrets
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.db.models import JSONField # Use JSONField for structured data

from core.models import User
from courses.models import Course, ClassSession

class AttendanceCode(models.Model):
    class_session = models.OneToOneField(ClassSession, on_delete=models.CASCADE, related_name='attendance_code')
    code = models.CharField(max_length=6, unique=True, default=lambda: secrets.token_hex(3).upper()) # 6-character hex code
    generated_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk: # Only set on creation
            self.expires_at = timezone.now() + timedelta(minutes=10) # 10-minute duration
        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"Code for {self.class_session}: {self.code}"

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course') # A student can enroll in a course only once

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.name}"

class AttendanceRecord(models.Model):
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    timestamp = models.DateTimeField(auto_now_add=True)
    is_present = models.BooleanField(default=False) # True after teacher validation
    # Fields for AI validation and geolocation from TypeScript code
    simulated_ip = models.CharField(max_length=45, blank=True, null=True) # Max IPv6 length
    simulated_geolocation = JSONField(blank=True, null=True) # Stores {"latitude": float, "longitude": float}
    ai_result = JSONField(blank=True, null=True) # Stores {"isFraudulent": bool, "fraudExplanation": str}

    class Meta:
        unique_together = ('class_session', 'student') # A student can only have one record per session
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.student.username} - {self.class_session.course.name} on {self.class_session.date} ({'Present' if self.is_present else 'Pending'})"