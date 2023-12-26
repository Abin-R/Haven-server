import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .models import *
from datetime import datetime

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_name = "general"
            self.room_group_name = f"chat_{self.room_name}"

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        except Exception as e:
            print(f"Error in connect method: {e}")
            # Add additional handling if needed
        else:
            print("Connection successful")


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')  # Change 'user' to 'message'
        username = self.scope["user"].username  # Assuming user is authenticated

        # Save message to the database if needed
        # Message.objects.create(sender=username, message_content=message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message_content': message,
                'user': username,
            }
        )

    async def chat_message(self, event):
        message = event['message_content']
        username = event['user']
        timestamp = datetime.now().isoformat()

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message_content': message,
            'sender': username,
            'timestamp': timestamp,
        }))
