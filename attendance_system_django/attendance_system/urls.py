# attendance_system/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import home, CustomLoginView, CustomLogoutView # Import your home view and custom login/logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), # Home page
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('attendance/', include('attendance.urls')),



    # Include app-specific URLs
    path('teacher/', include('attendance.urls')), # All teacher and student URLs handled by attendance app
    path('student/', include('attendance.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)