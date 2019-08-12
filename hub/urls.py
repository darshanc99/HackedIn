#Import Dependencies
from django.urls import path
from django.conf.urls import url,include
from . import views

urlpatterns = [
	#/hackedin/news/
	path('news/',views.news,name='news'),
	#/hackedin/
	path('',views.network,name='network'),
]