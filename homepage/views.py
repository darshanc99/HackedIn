#Import Dependencies
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

def homepage(request):
	return render(request,'homepage/homepage.html')