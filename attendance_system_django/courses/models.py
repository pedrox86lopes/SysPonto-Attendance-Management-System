# courses/models.py
from django.db import models
from core.models import User # Import your custom User model

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    teachers = models.ManyToManyField(User, related_name='courses_taught', limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return self.name

class ClassSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.course.name} - {self.date} {self.start_time}"

    class Meta:
        unique_together = ('course', 'date', 'start_time') # Ensure no duplicate sessions
        ordering = ['date', 'start_time']