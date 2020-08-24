from rest_framework import serializers

from chats.models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['chat_room', 'sender', 'message', 'timestamp']