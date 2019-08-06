#Import Dependencies
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
import ast

# Create your views here.
def news(request):
	#return HttpResponse("This is our latest News page")
	url = "https://hacker-news.firebaseio.com/v0/topstories.json"
	payload = "{}"
	response = requests.request("GET", url, data=payload)
	a = response.text
	#print(type(a))

	#Converting string list into list
	a = ast.literal_eval(a)
	context = {}
	key = "title"
	key1 = "url"
	key2 = "type"
	context.setdefault(key, [])
	context[key1] = []
	context[key2] = []
	context['n'] = []
	lis = []
	print(context)
	for i in range(0,3):
		url = "https://hacker-news.firebaseio.com/v0/item/"+str(a[i])+ ".json"
		payload = "{}"
		response = requests.request("GET", url, data=payload)
		dict_response = response.json()
		print(dict_response['title'])
		context[key].append((dict_response['title']))
		context[key1].append(dict_response['url'])
		context[key2].append(dict_response['type'])
		context['n'].append(i)
	print(context)
	template = loader.get_template('hub/index.html')
	return HttpResponse(template.render(context,request))