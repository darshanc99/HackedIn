#Import Dependencies
from django import forms
from .models import Topic, Post

#Forms

#Form for New Topic
class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(),
        max_length=4000,
        help_text='Max length of the text is 4000 characters'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']

#Form for New Post Form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]
        help_texts = {'message': 'Max length of the text is 4000 characters'}