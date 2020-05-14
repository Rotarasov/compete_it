from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from events.models import Event
from events.serializers import EventSerializer
from rest_framework import status


class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        min_date = query_params.get('min_date', None)
        max_date = query_params.get('max_date', None)
        type = query_params.get('type', None)
        events = Event.objects.all()
        return events


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer










