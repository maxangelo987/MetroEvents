from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum
# Create your models here.

class UserProfile(models.Model):
    contactno = models.CharField(max_length=20)
    birthday = models.CharField(max_length=20)
    is_organizer = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta:
    	db_table = "User"
    	verbose_name_plural = "Users"

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    datetime = models.DateTimeField()
    is_cancelled = models.BooleanField(default=False)
    address = models.CharField(max_length=200)

    organizers = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='organized_events')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='joined_events')

    class Meta:
    	db_table = "Event"
    	verbose_name_plural = "Events"



