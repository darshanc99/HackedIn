#Import Dependencies
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests,ast

#Views

#View function to render news
def news(request):
	url = "https://hacker-news.firebaseio.com/v0/topstories.json"
	payload = "{}"
	response = requests.request("GET", url, data=payload)
	a = response.text
	#Converting string list into list
	a = ast.literal_eval(a)
	lis = []
	ses = requests.session()
	for i in range(30):
		url = "https://hacker-news.firebaseio.com/v0/item/"+str(a[i])+ ".json"
		payload = "{}"
		response = ses.request("GET", url, data=payload)
		dict_response = response.json()
		if 'url' in dict_response:
			news = {'title': str(dict_response['title']), 'url': dict_response['url'], 'type': str(dict_response['type'])}
		
			lis.append(news)
	a = {'my_list':lis}
	template = loader.get_template('news/news.html')
	return HttpResponse(template.render(a,request))