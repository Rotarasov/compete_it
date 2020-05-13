from rest_framework import serializers
from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event

    def validate(self, data):
        """
        Check the start date to be before end date
        """
        if data.get('start_date') >= data.get('end_date'):
            raise serializers.ValidationError('End date must be greater than start date')
        return data


