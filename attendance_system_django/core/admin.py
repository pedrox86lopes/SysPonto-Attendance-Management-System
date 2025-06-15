# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User # Import your custom User model

# Deregister the default Group admin to manage groups through your custom UserAdmin if needed
# Or you can leave it registered if you want separate management for Groups.
# For simplicity, we'll keep it separate unless explicitly asked to integrate.
# admin.site.unregister(Group) # Uncomment if you want to completely control group management here


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom Admin interface for the User model.
    Extends Django's default UserAdmin to include the 'role' field.
    """
    # Define which fields are displayed in the list view of users
    list_display = BaseUserAdmin.list_display + ('role',)
    # Add 'role' to the filters sidebar
    list_filter = BaseUserAdmin.list_filter + ('role',)
    # Add 'role' to the fields when adding/changing a user
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    # Define which fields are searchable
    search_fields = ('username', 'email', 'role',)

