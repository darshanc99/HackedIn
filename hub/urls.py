#Import Dependencies
from django.urls import path
from django.conf.urls import url,include
from . import views

urlpatterns = [
	#/hackedin/technews/
	path('technews/',views.news,name='news'),
]