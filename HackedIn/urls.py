#Import Dependencies
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url,include
from users import views as user_views
from django.conf.urls.static import static
from users import views as user_views
from django.conf import settings

#URL Patterns
urlpatterns = [
	#/admin/
    path('admin/', admin.site.urls),
    #/
    path('',include('homepage.urls'),name='home'),
    #/news/
    path('news/',include('news.urls'),name='news'),
    #/jobs/
    path('jobs/',include('jobs.urls'),name='job'),
    #/forums/
    path('forums/',include('forums.urls'),name='forum'),
    #/community/
    path('community/',include('hub.urls'),name='community'),
    #/register/
    path('register/',user_views.register,name='register'),
    #/login/
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    #/logout/
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    #/profile/
    path('profile/',user_views.profile,name='profile'),
    #/profile/accomplishments/
    path('profile/accomplishments/',user_views.accomplishments,name='profacc'),
    #/profile/edit/
    path('profile/edit/',user_views.edit,name='profile-edit'),
    #/profile/applications/
    path('profile/applications/',user_views.applications,name='applications'),
    #/profile/offers/
    path('profile/offers/',user_views.offers,name='joboffers'),
    #/profile/candidates/
    path('profile/candidates/',user_views.candidates,name='jobcandidates'),
    #/profile/converstaions/
    path('profile/converstaions/',user_views.user_conversations,name='jobconv'),
    #/profile/github/<username>/
    path('profile/github/<str:username>',user_views.github,name='profgit'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)