from rest_framework import generics
from rest_framework.response import Response
from events.models import Event
from events.serializers import EventSerializer
from datetime import datetime


class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        min_date_str = query_params.get('min_date', False)
        max_date_str = query_params.get('max_date', False)
        event_type = query_params.get('type', False)
        if min_date_str:
            min_date = datetime.strptime(''.join([min_date_str, ':UTC']), '%d.%m.%Y:%Z')
            queryset = queryset.filter(start_date__gte=min_date)
        if max_date_str:
            max_date = datetime.strptime(''.join([max_date_str, ':UTC']), '%d.%m.%Y:%Z')
            queryset = queryset.filter(start_date__lte=max_date)
        if event_type:
            queryset = queryset.filter(type=event_type.lower())
        return queryset


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer











