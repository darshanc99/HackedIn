#Import Dependencies
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
#from django.http import HttpResponse
from django.template import loader
from .models import Accomplishment
from django.views.generic import (ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
	)
import requests

#Views

#Community
"""@login_required
def network(request):
	context = {
	'accomplishments' : Accomplishment.objects.all()
	}
	return render(request,'hub/network.html',context)"""

#Community
class PostListView(LoginRequiredMixin,ListView):
	model = Accomplishment
	template_name = 'hub/network.html' #<app>/<model>_<viewtype>.html
	context_object_name = 'accomplishments'
	ordering = ['-date_posted']
	paginate_by = 4

#User Specific List of Posts
class UserPostListView(LoginRequiredMixin,ListView):
	model = Accomplishment
	template_name = 'hub/user_posts.html' #<app>/<model>_<viewtype>.html
	context_object_name = 'accomplishments'
	paginate_by = 4

	def get_queryset(self):
		user = get_object_or_404(User,username=self.kwargs.get('username'))
		return Accomplishment.objects.filter(author=user).order_by('-date_posted')

#Details of a selected post
class PostDetailView(LoginRequiredMixin,DetailView):
	model = Accomplishment
	template_name = 'hub/networkpost.html'

#Create a new Post
class PostCreateView(LoginRequiredMixin,CreateView):
	model = Accomplishment
	fields = ['title','content']
	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	template_name = 'hub/post_form.html'

#Update the Post
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Accomplishment
	fields = ['title','content']
	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	def test_func(self):
		accomplishments = self.get_object()
		if self.request.user == accomplishments.author:
			return True
		return False

	template_name = 'hub/post_form.html'

#Delete a Post
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Accomplishment
	success_url = '/community'
	template_name = 'hub/networkpost.html'
	def test_func(self):
		accomplishments = self.get_object()
		if self.request.user == accomplishments.author:
			return True
		return False
	template_name = 'hub/post_confirm_delete.html'