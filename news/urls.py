#Import Dependencies
from django.urls import path
from . import views

#URL Patterns
urlpatterns = [
	#/news/
	path('',views.news,name='news'),
]