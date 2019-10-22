#Import Dependencies
from django.contrib import admin
from .models import Board, Topic, Post

#Register the Tables
admin.site.register((Board, Topic, Post))