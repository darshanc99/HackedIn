#Import Dependencies
from django.conf.urls import url
from . import views

#App Name
app_name = 'jobs'

#URL Patterns
urlpatterns = [
    #/jobs/
    url(r'^$', views.index, name='index'),

    #/jobs/offers/
    url(r'^offers/$', views.job_offers, name='job_offers'),

    #/jobs/offers/<offerid>/
    url(r'offers/(?P<offer_id>[0-9]+)/$', views.offer_detail, name='offer_detail'),    

    #/jobs/offers/<offer_id>/apply/
    url(r'offers/(?P<offer_id>[0-9]+)/apply/$', views.job_apply, name='job_apply'),

    #/jobs/offers/<offerid>/add/
    url(r'offers/add/$', views.job_offer_add, name='job_offer_add'),    

    #/jobs/offers/<id>/delete/
    url(r'offers/(?P<offer_id>[0-9]+)/delete/$', views.offer_delete, name='offer_delete'),

    #/jobs/offers/update/
    url(r'offers/(?P<offer_id>[0-9]+)/update/$', views.offer_update, name='offer_update'),

    #/jobs/applications/<id>
    url(r'applications/(?P<application_id>[0-9]+)/$', views.application_detail, name='application_detail'),

    #/jobs/applications/<id>/create_conversation/
    url(r'applications/(?P<application_id>[0-9]+)/create_conversation/$', views.create_conversation, name='create_conversation'),

    #/jobs/search/
    url(r'search/$', views.search, name='search'),
    
    #/jobs/messages/<id>/delete/
    url(r'^messages/(?P<conversation_id>[0-9]+)/delete$', views.conversation_delete, name='conversation_delete'),
    
    #/jobs/messages/<id>/
    url(r'^messages/(?P<conversation_id>[0-9]+)/$', views.conversation, name='conversation'),
    
    #/jobs/users/<name>/
    url(r'^users/(?P<username>\w+)/$', views.user_profile, name='user_profile'),

    #/jobs/users/<name>/applications/
    url(r'^users/(?P<username>\w+)/applications', views.user_applications, name='user_applications'),
    
    #/jobs/users/<name>/offers/
    url(r'^users/(?P<username>\w+)/offers', views.user_offers, name='user_offers'),

    #/jobs/users/<name>/candidates/
    url(r'^users/(?P<username>\w+)/candidates', views.candidates, name='candidates'),       

    #/jobs/users/<name>/conversations/
    url(r'^users/(?P<username>\w+)/conversations/$', views.user_conversations, name='user_conversations'),
]