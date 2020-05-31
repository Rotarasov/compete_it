from django.db import models
from users.models import User


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

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['start_date']


class Participation(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passed_survey = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.event.title} - {self.user.get_full_name()}'


class SurveyQuestion(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class SurveyAnswer(models.Model):
    ANSWER_TYPES = [
        (True, 'Да'),
        (False, 'Нет')
    ]

    participation = models.ForeignKey('Participation', on_delete=models.CASCADE)
    question = models.ForeignKey('SurveyQuestion', on_delete=models.CASCADE)
    answer = models.BooleanField(choices=ANSWER_TYPES)

    def __str__(self):
        return f'{self.participation} - {self.question.text}'


class TeamApplication(models.Model):
    participation = models.OneToOneField('Participation', on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.participation}'
