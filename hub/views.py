#Import Dependencies
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
import requests
import ast
from .models import Accomplishment

def news(request):
	#return HttpResponse("This is our latest News page")
	url = "https://hacker-news.firebaseio.com/v0/topstories.json"
	payload = "{}"
	response = requests.request("GET", url, data=payload)
	a = response.text
	#Converting string list into list
	a = ast.literal_eval(a)
	lis = []
	for i in range(10):
		url = "https://hacker-news.firebaseio.com/v0/item/"+str(a[i])+ ".json"
		payload = "{}"
		response = requests.request("GET", url, data=payload)
		dict_response = response.json()
		if 'url' in dict_response:
			news = {'title': str(dict_response['title']), 'url': dict_response['url'], 'type': str(dict_response['type'])}
		
			lis.append(news)
	print(lis)
	a = {'my_list':lis}
	#print(a)
	template = loader.get_template('hub/news.html')
	return HttpResponse(template.render(a,request))

@login_required
def network(request):
	context = {
	'accomplishments' : Accomplishment.objects.all()
	}
	return render(request,'hub/network.html',context)