from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from events.filters import EventFilter
from events import models
from events import serializers
from django.shortcuts import get_object_or_404


class EventList(generics.ListCreateAPIView):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description', 'type']


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer


class SurveyQuestionList(generics.ListCreateAPIView):
    serializer_class = serializers.SurveyQuestionSerializer

    def get_queryset(self):
        event = get_object_or_404(models.Event, pk=self.kwargs.get('event_pk'))
        user = self.request.user
        return models.SurveyQuestion.objects.filter(event=event)










