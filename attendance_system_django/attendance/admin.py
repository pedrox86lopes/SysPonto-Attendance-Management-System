# attendance/admin.py

from django.contrib import admin
from .models import AttendanceCode, AttendanceRecord, Enrollment, AbsenceJustification

@admin.register(AttendanceCode)
class AttendanceCodeAdmin(admin.ModelAdmin):
    """
    Admin interface for AttendanceCode.
    Customizes display, filters, and read-only fields.
    """
    list_display = ('code', 'class_session', 'created_at', 'expires_at', 'is_valid')
    list_filter = ('class_session__course', 'class_session__date')
    search_fields = ('code', 'class_session__course__name')
    readonly_fields = ('created_at', 'expires_at', 'is_valid') # These fields are automatically set

    # Override save_model to ensure code and expiry are generated if not present
    def save_model(self, request, obj, form, change):
        if not obj.pk: # Only on creation
            # Ensure code and expires_at are set if not automatically by model's save method
            if not obj.code:
                obj.save() # Call obj.save() to trigger code and expiry generation in model
            else:
                super().save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change)

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    """
    Admin interface for AttendanceRecord.
    Customizes display, filters, and actions.
    """
    list_display = ('student', 'class_session', 'timestamp', 'is_present', 'ai_result_status')
    list_filter = ('is_present', 'class_session__course', 'class_session__date', 'student__role')
    search_fields = ('student__username', 'class_session__course__name', 'simulated_ip')
    readonly_fields = ('timestamp', 'simulated_ip', 'simulated_geolocation', 'ai_result')
    date_hierarchy = 'timestamp' # For date-based drilldown

    # Custom method to display AI result status
    @admin.display(description='AI Status', boolean=True)
    def ai_result_status(self, obj):
        if obj.ai_result is None:
            return None # Use None to represent a grey/unknown status in boolean field
        return not obj.ai_result.get('isFraudulent', False) # True means "Looks OK", False means "Fraud"

    # Add actions to mark attendance as present
    actions = ['mark_as_present']

    @admin.action(description='Mark selected attendance records as Present')
    def mark_as_present(self, request, queryset):
        updated_count = queryset.update(is_present=True)
        self.message_user(
            request,
            f'{updated_count} attendance records were successfully marked as Present.',
            level='success'
        )

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    Admin interface for Enrollment.
    Customizes display and filters.
    """
    list_display = ('student', 'course', 'enrollment_date')
    list_filter = ('course', 'student')
    search_fields = ('student__username', 'course__name')
    readonly_fields = ('enrollment_date',)
    
@admin.register(AbsenceJustification)
class AbsenceJustificationAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_session', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at', 'class_session__course')
    search_fields = ('student__username', 'class_session__course__name')
    readonly_fields = ('submitted_at',)
