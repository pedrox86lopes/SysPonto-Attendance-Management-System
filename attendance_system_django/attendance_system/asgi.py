# attendance_system/asgi.py

import os

from django.core.asgi import get_asgi_application

# IMPORTANT: This line MUST come BEFORE importing any Django models or other
# code that relies on Django settings being configured.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# Now that Django settings and apps are ready, import Channels components
# and your app's routing.
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

# Import your routing configuration from your attendance app AFTER Django is set up
import attendance.routing


application = ProtocolTypeRouter({
    "http": django_asgi_app, # Handles regular HTTP requests
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack( # Handles Django authentication for WebSockets
            URLRouter( # Routes WebSocket connections
                attendance.routing.websocket_urlpatterns # Your WebSocket URL patterns
            )
        )
    ),
})
