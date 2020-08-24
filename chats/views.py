from rest_framework import generics, permissions

from chats import serializers, models
from users.models import User

class MessageList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        sender = self.request.user
        recipient = generics.get_object_or_404(User, id=self.kwargs['recipient_id'])
        chat_room = (models.ChatRoom.objects.filter(members=sender) &
                     models.ChatRoom.objects.filter(members=recipient)).first()
        return models.Message.objects.filter(chat_room=chat_room)