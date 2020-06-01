from rest_framework import generics, permissions, status
from rest_framework.response import Response

from chats import serializers, models
from users.models import User

class MessageList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        sender = generics.get_object_or_404(User, id=self.kwargs['sender_id'])
        receiver = generics.get_object_or_404(User, id=self.kwargs['receiver_id'])
        return models.Message.objects.filter(sender=sender, receiver=receiver)

    def create(self, request, *args, **kwargs):
        data = {'sender': self.kwargs['sender_id'], 'receiver': self.kwargs['receiver_id'], **request.data}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)