#Import Dependencies
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

#Forms

#Form for user registration
class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ['username','first_name','last_name','email','password1','password2']

#Form for updating user information - [user,email]
class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username','email']

#Form for updating user information - [image]
class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']