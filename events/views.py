from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from events.filters import EventFilter
from events import models
from events import serializers


class EventList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description', 'type']


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()


class SurveyList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.SurveyQuestionSerializer

    def get_queryset(self):
        event = generics.get_object_or_404(models.Event, pk=self.kwargs.get('event_pk'))
        user = self.request.user
        return models.SurveyQuestion.objects.filter(user=user, event=event)










