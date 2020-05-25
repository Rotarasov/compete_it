from django.db import models
from django.contrib.auth.models import User


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
    participants = models.ManyToManyField(User)

    class Meta:
        ordering = ['start_date']


class SurveyAnswer(models.Model):
    ANSWER_TYPES = [
        (True, 'Да'),
        (False, 'Нет')
    ]

    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('SurveyQuestion', on_delete=models.CASCADE)
    answer = models.BooleanField(choices=ANSWER_TYPES)


class SurveyQuestion(models.Model):
    text = models.CharField(max_length=200)


class TeamApplication(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
