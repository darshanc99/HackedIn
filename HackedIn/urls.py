#Import Dependencies
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from users import views as user_views

urlpatterns = [
	#/admin/
    path('admin/', admin.site.urls),
    #/register/
    path('register/',user_views.register,name='register'),
    #/hackedin/
    path('hackedin/',include('hub.urls'),name='home'),
]