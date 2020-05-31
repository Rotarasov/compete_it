from rest_framework import generics, permissions, status
from rest_framework.response import Response

from chats import serializers, models

# class MessageList(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializers.MessageSerializer
#     queryset = models.Message.objects.all()
#
#     def list(self, request, *args, **kwargs):
#
