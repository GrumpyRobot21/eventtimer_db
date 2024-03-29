from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    name = models.CharField(max_length=100, default='Not Provided')
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

class Event(models.Model):
    eventCategory = models.CharField(max_length=100)
    details = models.TextField()
    duration = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.eventCategory

    