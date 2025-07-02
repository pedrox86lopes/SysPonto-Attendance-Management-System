# attendance/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .views import send_group_notification


class ClassSessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.class_session_id = self.scope['url_route']['kwargs']['class_session_id']
        self.class_session_group_name = f'class_session_{self.class_session_id}_notifications'

        # Join class session group
        await self.channel_layer.group_add(
            self.class_session_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave class session group
        await self.channel_layer.group_discard(
            self.class_session_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (from client)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        # Send message to class session group
        await self.channel_layer.group_send(
            self.class_session_group_name,
            {
                'type': 'class_session_message',
                'message': message
            }
        )

    # Receive message from class session group (from backend via send_group_notification)
    async def class_session_message(self, event):
        message = event['message']
        context = event.get('context', {})

        # Send message to WebSocket client
        await self.send(text_data=json.dumps({
            'type': 'class_session_message',
            'message': message,
            'context': context
        }))

    # Handle specific message types from your views
    async def student_submitted(self, event):
        """Handle when a student submits attendance"""
        await self.send(text_data=json.dumps({
            'type': 'class_session_message',
            'message': event['message'],
            'context': {
                'type': 'student_submitted',
                **event['context']
            }
        }))

    async def ai_result_updated_for_teacher(self, event):
        """Handle AI validation results"""
        await self.send(text_data=json.dumps({
            'type': 'class_session_message', 
            'message': event['message'],
            'context': {
                'type': 'ai_result_updated_for_teacher',
                **event['context']
            }
        }))

    async def code_generated_for_teacher(self, event):
        """Handle when a new attendance code is generated"""
        await self.send(text_data=json.dumps({
            'type': 'class_session_message',
            'message': event['message'],
            'context': {
                'type': 'code_generated_for_teacher',
                **event['context']
            }
        }))

    async def attendance_validated(self, event):
        """Handle when attendance is validated by teacher"""
        await self.send(text_data=json.dumps({
            'type': 'class_session_message',
            'message': event['message'],
            'context': {
                'type': 'attendance_validated',
                **event['context']
            }
        }))


class StudentNotificationConsumer(AsyncWebsocketConsumer):
    """Consumer for student-specific notifications"""
    
    async def connect(self):
        # Create a general student notification group
        self.group_name = 'student_notifications'
        
        # Join the student notifications group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the student notifications group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket (from client)
    async def receive(self, text_data):
        # Students typically don't send messages, just receive notifications
        pass

    # Handle attendance validation notifications
    async def attendance_validated(self, event):
        """Handle when a student's attendance is validated"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message'],
            'context': event.get('context', {})
        }))