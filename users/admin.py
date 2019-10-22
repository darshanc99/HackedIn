#Import Dependencies
from django.contrib import admin
from .models import Profile

#Registering the Profile table to appear on the admin interface
admin.site.register(Profile)