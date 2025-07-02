# attendance/routing.py
from django.urls import re_path
from attendance import consumers 

websocket_urlpatterns = [
    re_path(r'ws/attendance/class_session_(?P<class_session_id>\w+)/$', consumers.ClassSessionConsumer.as_asgi()),
    # Now StudentNotificationConsumer is implemented
    re_path(r'ws/student/notifications/$', consumers.StudentNotificationConsumer.as_asgi()),
]