from django.utils import timezone
from django.db import models

from compete_it import settings

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=255)
    timestamp = models.TimeField(default=timezone.now)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
