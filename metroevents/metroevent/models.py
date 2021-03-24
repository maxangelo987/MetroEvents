from django.conf import settings
from django.db import models
from enum import Enum
from django.utils import timezone
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
    address = models.CharField(max_length=200)
    event_pic = models.ImageField(upload_to='media/')
    is_cancelled = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    organizers = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='organized_events')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='joined_events')

    class Meta:
    	db_table = "Event"
    	verbose_name_plural = "Events"

class Request(models.Model):
    request_type = models.CharField(max_length= 150, default="", blank=True, null=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')

    user_type = models.CharField(max_length= 150, default="", blank=True, null=True)

    event_id= models.ForeignKey(Event, on_delete=models.CASCADE, related_name='events')

    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default= timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Request"


