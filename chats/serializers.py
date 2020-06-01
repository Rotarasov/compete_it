from rest_framework import serializers

from users.models import User
from chats.models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field=lambda obj: obj.get_full_name(), queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(slug_field=lambda obj: obj.get_full_name(), queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']