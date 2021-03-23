from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from metroevent.models import Event


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name','last_name','username', 'email', 'password1', 'password2']

class EventForm(forms.ModelForm):
	class Meta:
 		model = Event
 		fields = ['name','description','datetime','address','event_pic']
    
