#Import Dependencies
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from .models import Accomplishment

@login_required
def network(request):
	context = {
	'accomplishments' : Accomplishment.objects.all()
	}
	return render(request,'hub/network.html',context)