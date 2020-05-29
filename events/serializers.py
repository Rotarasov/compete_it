from rest_framework import serializers
from events import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'

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
