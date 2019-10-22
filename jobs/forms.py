#Import Dependencies
from django import forms
from django.forms import Textarea
from django.utils.translation import gettext as _
from .models import *

#Forms

#JobOfferForm
class JobOfferForm(forms.ModelForm):

    class Meta:
        model = JobOffer
        fields = ['industry', 'avatar', 'title', 'companyName', 'aboutUs', 'jobDescription', 'requirements',
                  'whatWeOffer', 'salary', 'location',]

        widgets = {
            'aboutUs': Textarea(attrs={'cols': 80, 'rows': 10}),
            'jobDescription': Textarea(attrs={'cols': 80, 'rows': 10}),
            'requirements': Textarea(attrs={'cols': 80, 'rows': 10}),
            'whatWeOffer': Textarea(attrs={'cols': 80, 'rows': 10}),
        }

        labels = {
            'avatar': _('Picture of Your Company'),
            'title': _('Title'),
            'companyName': _('Company Name'),
            'aboutUs': _('About Your Company'),
            'jobDescription': _('Description of the Job'),
            'requirements': _('Requirements'),
            'whatWeOffer': _('What we Offer'),
            'salary': _('Salary'),
            'location': _('Location'),
        }

        help_texts = {
            'avatar': _('best resolution: 16:9'),
            'title': _('job name (search sensitive)'),
            'aboutUs': _('company name, people, what is your products etc.'),
            'jobDescription': _('responsibilities, working hours etc. ("-" is new point)'),
            'requirements': _('what skills candidate should have ("-" is new point)'),
            'whatWeOffer': _('health care, free lunch etc. ("-" is new point)'),
            'salary': _('monthly (in $)'),
            'location': _('city, street (search sensitive)'),
        }

#ApplicationForm
class ApplicationForm(forms.ModelForm):

    class Meta:
        model = ApplicationRequirements
        fields = ['formPicture', 'formAge', 'formEducation', 'formPlaceOfResidence',
                  'formAboutYou', 'formCurrentStatus', 'formLanguages', 'formExperience', 'formHobby']

        labels = {
            'formPicture': _('Picture of Candidate.'),
            'formAge': _('Age of Candidate.'),
            'formEducation': _('Education of Candidate.'),
            'formPlaceOfResidence': _('Living Place of Candidate.'),
            'formAboutYou': _('Section "About".'),
            'formCurrentStatus': _('Current working status of Candidate.'),
            'formLanguages': _('Languages that Candidate knows.'),
            'formExperience': _('Previous experience of Candidate.'),
            'formHobby': _('Hobby of Candidate.'),
        }

#JobApply Form
class JobApplyForm(forms.ModelForm):

    class Meta:
        model = JobApplication
        fields = ['name', 'surname', 'email', 'picture', 'age', 'education', 'placeOfResidence',
                  'currentStatus', 'aboutYou', 'languages', 'experience', 'hobby',]

        labels = {
            'name': _('Name'),
            'surname': _('Last Name'),
            'email': _('Contact Email'),
            'picture': _('Picture of Yourself'),
            'age': _('Your Age'),
            'education': _('Your Education'),
            'placeOfResidence': _('Place of Residence'),
            'currentStatus': _('Your current work status'),
            'aboutYou': _('Tell us something about Yourself'),
            'languages': _('Languages you know'),
            'experience': _('Your experience'),
            'hobby': _('What is your hobby?'),
        }

        help_texts = {
            'experience': _('Your skills and previous workplace.'),
            'languages': _('best pattern: "-language(level)" + new line'),
        }

        widgets = {
            'experience': Textarea(attrs={'cols': 80, 'rows': 10}),
            'languages': Textarea(attrs={'cols': 80, 'rows': 5}),
            'aboutYou': Textarea(attrs={'cols': 80, 'rows': 10}),
            'hobby': Textarea(attrs={'cols': 80, 'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(JobApplyForm, self).__init__(*args, **kwargs)

        if extra:
            for field, value in extra.items():
                if not value:
                    self.fields['%s' % field].widget = forms.HiddenInput()

#Conversation Form
class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['title']

#Message Form
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']