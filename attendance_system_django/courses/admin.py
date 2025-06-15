# courses/admin.py

from django.contrib import admin
from .models import Course, ClassSession

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin interface for the Course model.
    Customizes list display and search functionality.
    """
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    # Filter by teachers related to the course
    list_filter = ('teachers',)
    # Use a horizontal filter for ManyToMany relationships for better UX
    filter_horizontal = ('teachers',)

@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    """
    Admin interface for the ClassSession model.
    Customizes list display, filters, and search.
    """
    list_display = ('course', 'date', 'start_time', 'end_time')
    list_filter = ('course', 'date')
    search_fields = ('course__name', 'date') # Allow searching by course name
    # Add a date hierarchy for easy navigation by date
    date_hierarchy = 'date'
