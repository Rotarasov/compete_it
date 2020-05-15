from django_filters import rest_framework as filters
from events.models import Event


class EventFilter(filters.FilterSet):
    min_date = filters.DateTimeFilter(field_name='start_date', lookup_expr='gte')
    max_date = filters.DateTimeFilter(field_name='start_date', lookup_expr='lte')
    event_type = filters.CharFilter(field_name='type', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['event_type', 'min_date', 'max_date']