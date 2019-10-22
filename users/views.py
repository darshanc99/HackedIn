#Import Dependencies
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from jobs.models import JobApplication, JobOffer, Conversation
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from hub.models import Accomplishment
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from django.template import loader
from django.http import HttpResponse
import requests

# Create your views here.

#View function for register
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f'Account created for {username}! You can now login :)')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request,'users/register.html',{'form':form})

#View function for profile
@login_required
def profile(request):
	context = {
	}
	return render(request,'users/profile.html',context)

#View function for editing the profile
@login_required
def edit(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST,instance=request.user)
		p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request,f'Your Account has been updated!')
			return redirect('profile')			

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
	'u_form' : u_form,
	'p_form' : p_form
	}
	return render(request,'users/profile-edit.html',context)

#View function for applications
@login_required
def applications(request):
    applications = []
    title = 'Your Applications'
    if request.user.is_authenticated:
        applications = JobApplication.objects.filter(user=request.user).order_by('-created_date')

    paginator = Paginator(applications, 10)
    page = request.GET.get('page')

    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)

    context = {
        'applications': applications,
        'title': title,
    }
    return render(request, 'users/user_applications.html', context)

#View function for offers
@login_required
def offers(request):
    offers = []
    if request.user.is_authenticated:
        offers = JobOffer.objects.filter(user=request.user).order_by('-created_date')
        paginator = Paginator(offers, 10)
        page = request.GET.get('page')

        try:
            offers = paginator.page(page)
        except PageNotAnInteger:
            offers = paginator.page(1)
        except EmptyPage:
            offers = paginator.page(paginator.num_pages)

    return render(request, 'users/useroffers.html', {'offers': offers})

#View function for candidates
@login_required
def candidates(request):
    applications = []
    title = 'Your Candidates'
    if request.user.is_authenticated:
        applications = JobApplication.objects.filter(job_offer__user=request.user).order_by('-created_date')

    paginator = Paginator(applications, 10)
    page = request.GET.get('page')

    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)

    context = {
        'applications': applications,
        'title': title,
    }
    return render(request, 'users/candidates.html', context)

#View function for user conversations
@login_required
def user_conversations(request):
    if request.user.is_authenticated:
        conversations = Conversation.objects.filter(
            Q(user_one=request.user) |
            Q(user_two=request.user)
        )
        context = {
            'conversations': conversations,
        }
        return render(request, 'users/user_conversations.html', context)

#View function for accomplishments
@login_required
def accomplishments(request):
    accomplishments = []
    if request.user.is_authenticated:
        accomplishments = Accomplishment.objects.filter(author=request.user)
        context = {
            'accomplishments':accomplishments,
        }
        return render(request,'users/accomplishments.html',context)

#View function for github repositories
@login_required
def github(request,username):
    #user = get_object_or_404(User,username=self.kwargs.get('username'))
    req = requests.get('https://api.github.com/users/'+username+'/repos?per_page=1000')
    json = req.json()
    lis = []
    for i in range(0,len(json)):
        #print("Project Number:",i+1)
        #print("Project Name:",json[i]['name'])
        #print("Project URL:",json[i]['svn_url'],"\n")
        git = {'number': str(i+1), 'name': str(json[i]['name']), 'url': str(json[i]['svn_url'])}
        lis.append(git)
    context = {
        'git' : lis
    }
    template = loader.get_template('users/github.html')
    return HttpResponse(template.render(context,request))