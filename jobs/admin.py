#Import Dependencies
from django.contrib import admin
from .models import *

#Register Tables to display on the Admin Interface
admin.site.register(JobOffer)
admin.site.register(ApplicationRequirements)
admin.site.register(JobApplication)
admin.site.register(Conversation)
admin.site.register(Message)