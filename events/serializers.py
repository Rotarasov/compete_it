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


class SurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SurveyAnswer
        fields = ['id', 'answer']


class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SurveyQuestion
        fields = '__all__'
