# attendance_system/routing.py (or wherever your WebSocket routes are defined)
from django.urls import re_path
from attendance import consumers 

websocket_urlpatterns = [
    re_path(r'ws/attendance/class_session/(?P<class_session_id>\w+)/$', consumers.ClassSessionConsumer.as_asgi()),
    # The teacher general group notification is also handled by this consumer
]