import json

from django.core.exceptions import ObjectDoesNotExist
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import ChatRoom, Message
from users.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        recipient_id = self.scope['url_route']['kwargs']['recipient_id']
        recipient = await self.get_recipient(recipient_id)
        sender = self.scope['user']

        if recipient:
            self.chat_room = await self.create_or_open_chat_room(sender, recipient)
            self.room_group_name = f'chat_{self.chat_room.id}'

            await self.channel_layer.group_add({
                self.room_group_name,
                self.channel_name
            })

            await self.accept()
        else:
            await self.close()


    @database_sync_to_async
    def create_or_open_chat_room(self, u1, u2):
        chat_room = (ChatRoom.objects.filter(members=u1) & ChatRoom.objects.filter(members=u2)).first()
        if not chat_room:
            chat_room = ChatRoom.objects.create()
            chat_room.members.add(u1, u2)
        return chat_room

    @database_sync_to_async
    def get_recipient(self, recipient_id):
        try:
            return User.objects.get(id=recipient_id)
        except ObjectDoesNotExist:
            return None

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']

        await self.save_message(sender_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'sender_id': sender_id,
                'message': message
            }
        )

    @database_sync_to_async
    def save_message(self, sender_id, message):
        Message.objects.create(chat_room_id=self.chat_room.id, sender_id=sender_id, message=message)


    async def chat_message(self, event):
        sender_id = event['sender_id']
        message = event['message']

        await self.send(text_data=json.dumps({
            'sender_id': sender_id,
            'message': message
        }))

