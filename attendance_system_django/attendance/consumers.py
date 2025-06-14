# attendance/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils import timezone
from django.db.models import F # Import F expression

# Import your models
from core.models import User
from courses.models import ClassSession, Course
from attendance.models import AttendanceRecord, AttendanceCode, Enrollment

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        # Each user gets a personal notification group
        self.user_group_name = f'user_{self.user.id}_notifications'
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        # Teachers join groups for their classes
        if self.user.role == 'teacher':
            teacher_classes = await self.get_teacher_class_session_ids(self.user)
            for class_session_id in teacher_classes:
                class_group_name = f'class_session_{class_session_id}_notifications'
                await self.channel_layer.group_add(
                    class_group_name,
                    self.channel_name
                )
            # Teachers also have a general group to get notifications about codes they generate
            await self.channel_layer.group_add(
                f'teacher_{self.user.id}_general_notifications',
                self.channel_name
            )


        # Students join groups for classes they are enrolled in
        elif self.user.role == 'student':
            student_enrolled_classes = await self.get_student_enrolled_class_session_ids(self.user)
            for class_session_id in student_enrolled_classes:
                class_group_name = f'class_session_{class_session_id}_notifications'
                await self.channel_layer.group_add(
                    class_group_name,
                    self.channel_name
                )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave all joined groups
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

        if self.user.role == 'teacher':
            teacher_classes = await self.get_teacher_class_session_ids(self.user)
            for class_session_id in teacher_classes:
                class_group_name = f'class_session_{class_session_id}_notifications'
                await self.channel_layer.group_discard(class_group_name, self.channel_name)
            await self.channel_layer.group_discard(f'teacher_{self.user.id}_general_notifications', self.channel_name)

        elif self.user.role == 'student':
            student_enrolled_classes = await self.get_student_enrolled_class_session_ids(self.user)
            for class_session_id in student_enrolled_classes:
                class_group_name = f'class_session_{class_session_id}_notifications'
                await self.channel_layer.group_discard(class_group_name, self.channel_name)


    # Receive message from channel layer (from Django views/signals)
    async def send_notification(self, event):
        message = event['message']
        notification_type = event['type']
        context = event.get('context', {})

        await self.send(text_data=json.dumps({
            'type': notification_type,
            'message': message,
            'context': context,
        }))

    # Helper functions to get user-specific class IDs (using sync_to_async for ORM queries)
    @sync_to_async
    def get_teacher_class_session_ids(self, teacher_user):
        # Get all ClassSession IDs taught by this teacher for today or future
        return list(ClassSession.objects.filter(
            course__teachers=teacher_user,
            date__gte=timezone.localdate()
        ).values_list('id', flat=True))

    @sync_to_async
    def get_student_enrolled_class_session_ids(self, student_user):
        # Get all ClassSession IDs for courses the student is enrolled in for today or future
        return list(ClassSession.objects.filter(
            course__enrollment__student=student_user,
            date__gte=timezone.localdate()
        ).values_list('id', flat=True))