#Import Dependencies
from django.urls import path
from django.conf.urls import url,include
from . import views
from .views import (
	PostListView,
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
	UserPostListView
	)

urlpatterns = [
	#/community/
	path('',PostListView.as_view(),name='network'),
	#/community/<pk>
	path('<int:pk>/',PostDetailView.as_view(),name='network-post'),
	#/community/new/
	path('new/',PostCreateView.as_view(),name='network-create'),
	#/community/<pk>/update/
	path('<int:pk>/update/',PostUpdateView.as_view(),name='network-update'),
	#/community/<pk>/delete/
	path('<int:pk>/delete/',PostDeleteView.as_view(),name='network-delete'),	
	#/community/user/<username>
	path('user/<str:username>',UserPostListView.as_view(),name='user-posts'),
]