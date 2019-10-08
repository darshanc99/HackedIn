from django.urls import path
from django.conf.urls import url,include
from . import views

urlpatterns = [
	url(r'^$', views.BoardListView.as_view(), name='home'),
    path('boards/<int:pk>/', views.TopicListView.as_view(), name='board_topics'),
    path('boards/<int:pk>/new/', views.new_topic, name='new_topic'),
    path('boards/<int:pk>/<int:topic_pk>/', views.PostListView.as_view(), name='topic_posts'),
    path('boards/<int:pk>/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    path('boards/<int:pk>/<int:topic_pk>/<int:post_pk>/edit', views.PostUpdateView.as_view(),
         name='edit_post'),
]
