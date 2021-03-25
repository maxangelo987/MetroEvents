from django.conf import settings
from django.db import models
from enum import Enum
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Create your models here.

#class UserProfile(models.Model):
#   contactno = models.CharField(max_length=20)
#    birthday = models.CharField(max_length=20)
#    is_organizer = models.BooleanField(default=False)
#    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

#    class Meta:
#    	db_table = "User"
#    	verbose_name_plural = "Users"

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    datetime = models.DateTimeField()
    address = models.CharField(max_length=200)
    event_pic = models.ImageField(upload_to='media/')
    is_cancelled = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    participants = models.ManyToManyField(User, blank=True)

    class Meta:
    	db_table = "Event"
    	verbose_name_plural = "Events"

class Request(models.Model):
    request_type = models.CharField(max_length= 150, default="", blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="sender")

    event= models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')

    status = models.CharField(max_length= 150, default="Pending", blank=True, null=True)
    created_at = models.DateTimeField(default= timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Request"


class Organizer(models.Model):
    organizer = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=0)
    event = models.ManyToManyField(Event, blank=True)
    date_promoted = models.DateField(auto_now_add=True, blank=True)

    class Meta:
        db_table = "Organizer"
    

class Administrator(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=0)
    event = models.ManyToManyField(Event, blank=True)

    class Meta:
        db_table = "Administrator"

        





