#Import Dependencies
from django.urls import path
from django.conf.urls import url,include
from . import views

#URL Patterns
urlpatterns = [
	#/
	url(r'^$', views.homepage, name='homepage'),
]