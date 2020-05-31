from django.forms.models import model_to_dict
from rest_framework import serializers
from events import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Dynamically set necessary fields
        """
        fields = kwargs.pop('fields')
        super(EventSerializer, self).__init__(*args, **kwargs)
        if fields != '__all__':
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate(self, data):
        """
        Check the start date to be before end date
        """
        if data.get('start_date') >= data.get('end_date'):
            raise serializers.ValidationError('End date must be greater than start date')
        return data


class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SurveyQuestion
        fields = '__all__'


class SurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SurveyAnswer
        fields = '__all__'


class TeamApplicationSerializer(serializers.ModelSerializer):
    participation_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.TeamApplication
        fields = ['participation', 'description', 'participation_info']

    def get_participation_info(self, obj):
        event = model_to_dict(obj.participation.event, fields=['id', 'title'])
        user = model_to_dict(obj.participation.user, fields=['id', 'first_name', 'last_name', 'email'])
        return {'event': event, 'user': user}


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Participation
        fields = ['user', 'event']
