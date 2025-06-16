# attendance/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ClassSessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.class_session_id = self.scope['url_route']['kwargs']['class_session_id']
        self.class_session_group_name = f'class_session_{self.class_session_id}'

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

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to class session group
        await self.channel_layer.group_send(
            self.class_session_group_name,
            {
                'type': 'class_session_message',
                'message': message
            }
        )

    # Receive message from class session group
    async def class_session_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))