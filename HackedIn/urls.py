#Import Dependencies
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url,include
from users import views as user_views
from django.conf.urls.static import static
from users import views as user_views
from django.conf import settings

urlpatterns = [
	#/admin/
    path('admin/', admin.site.urls),
    #/register/
    path('register/',user_views.register,name='register'),
    #/community/
    path('community/',include('hub.urls'),name='home'),
    #/news/
    path('news/',include('news.urls'),name='news'),
    #/login/
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    #/logout/
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    #/profile/
    path('profile/',user_views.profile,name='profile'),
    #/
    path('',include('homepage.urls')),
    #/forums/
    path('forums/',include('forums.urls')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)