from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Event)
admin.site.register(Request)
admin.site.register(Organizer)
admin.site.register(Administrator)