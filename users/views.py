#Import Dependencies
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from jobs.models import JobApplication, JobOffer, Conversation
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
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

@login_required
def profile(request):
	context = {
	}
	return render(request,'users/profile.html',context)

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