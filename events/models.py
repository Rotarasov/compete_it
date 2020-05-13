from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Event(models.Model):
    EVENTS_TYPES = [
        ('contest', 'Contest'),
        ('hackathon', 'Hackathon')
    ]

    title = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=200, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    type = models.CharField(max_length=9, choices=EVENTS_TYPES)
    image = models.ImageField(upload_to='event_pics')
    link = models.URLField(max_length=200)


class SurveyQuestion(models.Model):
    ANSWER_TYPES = [
        (True, 'Да'),
        (False, 'Нет')
    ]

    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    answer = models.BooleanField(choices=ANSWER_TYPES)


class TeamApplication(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
