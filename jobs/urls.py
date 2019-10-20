from django.conf.urls import url
from . import views

app_name = 'jobs'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/(?P<username>\w+)/$', views.user_profile, name='user_profile'),
    url(r'^offers/$', views.job_offers, name='job_offers'),
    url(r'offers/add/$', views.job_offer_add, name='job_offer_add'),
    url(r'offers/(?P<offer_id>[0-9]+)/$', views.offer_detail, name='offer_detail'),
    url(r'offers/(?P<offer_id>[0-9]+)/apply/$', views.job_apply, name='job_apply'),
    url(r'^users/(?P<username>\w+)/$', views.user_profile, name='user_profile'),
    url(r'^users/(?P<username>\w+)/applications', views.user_applications, name='user_applications'),
    url(r'^users/(?P<username>\w+)/offers', views.user_offers, name='user_offers'),
    url(r'^users/(?P<username>\w+)/candidates', views.candidates, name='candidates'),
    url(r'applications/(?P<application_id>[0-9]+)/$', views.application_detail, name='application_detail'),
    url(r'offers/(?P<offer_id>[0-9]+)/delete/$', views.offer_delete, name='offer_delete'),
    url(r'offers/(?P<offer_id>[0-9]+)/update/$', views.offer_update, name='offer_update'),
    url(r'search/$', views.search, name='search'),
    url(r'applications/(?P<application_id>[0-9]+)/create_conversation/$', views.create_conversation, name='create_conversation'),
    url(r'^users/(?P<username>\w+)/conversations/$', views.user_conversations, name='user_conversations'),
    url(r'^messages/(?P<conversation_id>[0-9]+)/delete$', views.conversation_delete, name='conversation_delete'),
    url(r'^messages/(?P<conversation_id>[0-9]+)/$', views.conversation, name='conversation'),
]