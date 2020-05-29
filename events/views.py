from rest_framework import generics, filters, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from events.filters import EventFilter
from events import models
from events import serializers


class EventList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description', 'type']

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['fields'] = ['id', 'title', 'start_date', 'type', 'image']
        return serializer_class(*args, **kwargs)




class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['fields'] = '__all__'
        return serializer_class(*args, **kwargs)


class SurveyList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.SurveyQuestionSerializer

    def get_queryset(self):
        event = generics.get_object_or_404(models.Event, pk=self.kwargs.get('event_pk'))
        user = self.request.user
        return models.SurveyQuestion.objects.filter(user=user, event=event)










