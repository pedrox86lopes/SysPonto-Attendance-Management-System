# attendance/models.py

from django.db import models
from core.models import User # Assuming User is in core
from courses.models import ClassSession, Course # Assuming these are in courses
from django.utils import timezone
import uuid # For generating UUIDs
import datetime # For timedelta

class AttendanceCode(models.Model):
    # 'code' is now blank=True, null=True, and generated in the save method
    code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    class_session = models.OneToOneField(ClassSession, on_delete=models.CASCADE, related_name='attendance_code')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Generate a unique 6-character uppercase alphanumeric code if not already set
        if not self.code:
            while True:
                # Generate a UUID and take the first 6 uppercase characters
                new_code = str(uuid.uuid4()).replace('-', '')[:6].upper()
                # Ensure the generated code is truly unique before saving
                if not AttendanceCode.objects.filter(code=new_code).exists():
                    self.code = new_code
                    break
        # Set expiry if not already set (e.g., 5 minutes from creation)
        if not self.expires_at:
            self.expires_at = timezone.now() + datetime.timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_valid(self):
        """Checks if the attendance code is currently active (not expired)."""
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"Code {self.code} for {self.class_session.course.name} on {self.class_session.date}"

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

