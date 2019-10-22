#Import Dependencies
from django.apps import AppConfig

#UsersConfig
class UsersConfig(AppConfig):
    name = 'users'

    #Init of signals
    def ready(self):
    	import users.signals