#Import Dependencies
from django.shortcuts import render

#Views

#Function to render Homepage
def homepage(request):
	return render(request,'homepage/homepage.html')