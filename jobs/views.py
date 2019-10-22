#Import Dependencies
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required

#Views
# Home Page
def index(request):
    return render(request, 'jobs/index.html', {})

#Post Message
@login_required
def post_message(request, conversation_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            messageForm = MessageForm(request.POST)
            conversation = get_object_or_404(Conversation, id=conversation_id)
            if messageForm.is_valid() \
                    and (conversation.user_one == request.user or conversation.user_two == request.user):
                message = messageForm.save(commit=False)
                message.user = request.user
                message.conversation = conversation
                message.content = request.POST.get('content')
                message.save()

        return redirect('jobs:conversation', conversation_id=conversation_id)

    return redirect('auth_login')

# Create Conversation
@login_required
def create_conversation(request, application_id):
    if request.user.is_authenticated:
        application = get_object_or_404(JobApplication, id=application_id)
        if request.user == application.job_offer.user:
            conversationForm = ConversationForm()
            conversation = conversationForm.save(commit=False)
            conversation.user_one = request.user
            conversation.user_two = application.user
            conversation.title = application.job_offer.title
            conversation.save()

            return redirect('jobs:conversation', conversation_id=conversation.id)

    return redirect('auth_login')

# Conversation
@login_required
def conversation(request, conversation_id):
    if request.method == 'POST':
        return post_message(request, conversation_id)

    if request.user.is_authenticated:
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if conversation.user_one == request.user or conversation.user_two == request.user:
            conversations = Conversation.objects.filter(
                Q(user_one=request.user) |
                Q(user_two=request.user)
            )
            messages = Message.objects.filter(conversation_id=conversation.id)
            paginator = Paginator(messages, 10)
            page = request.GET.get('page')

            try:
                messages = paginator.page(page)
            except PageNotAnInteger:
                messages = paginator.page(1)
            except EmptyPage:
                messages = paginator.page(paginator.num_pages)

            context = {
                'messages': messages,
                'conversation': conversation,
                'conversations': conversations,
            }
            return render(request, 'jobs/conversation.html', context)

    return redirect('auth_login')


# Delete Conversation
@login_required
def conversation_delete(request, conversation_id):
    if request.user.is_authenticated:
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if conversation.user_one == request.user or conversation.user_two == request.user:
            conversation.delete()
            return redirect('jobs:user_conversations', username=request.user.username)

    return redirect('auth_login')


# User Conversations
@login_required
def user_conversations(request, username):
    if request.user.is_authenticated:
        conversations = Conversation.objects.filter(
            Q(user_one=request.user) |
            Q(user_two=request.user)
        )
        context = {
            'conversations': conversations,
        }
        return render(request, 'jobs/user_conversations.html', context)


# Search
def search(request):
    offers = None
    title = 'Search for: '
    if (('title' in request.GET) and request.GET['title'].strip()) \
            or (('location' in request.GET) and request.GET['location'].strip()) \
            or (('industry' in request.GET) and request.GET['industry'].strip()):

        queryTitle = request.GET['title']
        queryLocation = request.GET['location']
        queryIndustry = request.GET['industry']
        title += queryTitle + ' ' + queryLocation + ' ' + queryIndustry

        offers = JobOffer.objects.filter(
            Q(title__icontains=queryTitle) &
            Q(location__icontains=queryLocation) &
            Q(industry__icontains=queryIndustry)
        )

    industries = JobOffer.INDUSTRY_TYPES
    context = {
        'title': title,
        'offers': offers,
        'industries': industries,
    }
    return render(request, 'jobs/offers.html', context)


# User Profile
@login_required
def user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'jobs/user_profile.html', {'user': user})


# Application Details
@login_required
def application_detail(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    if request.user.is_authenticated and \
            (application.job_offer.user == request.user or application.user == request.user):
        languages = None
        if application.languages:
            languages = application.languages.rstrip().split('-')
            #print(languages)
            languages =  filter(None, languages)
        context = {
            'languages': languages,
            'application': application,
        }
        return render(request, 'jobs/application_detail.html', context)

    return redirect('jobs:index')


# Delete Offer
@login_required
def offer_delete(request, offer_id):
    offer = get_object_or_404(JobOffer, id=offer_id)
    if request.user.is_authenticated and offer.user == request.user:
        offer.delete()
        return redirect('/jobs/offers/', username=request.user.username)

    return redirect('jobs:index')

# Update Offer
@login_required
def offer_update(request, offer_id):
    title = ''
    offer = get_object_or_404(JobOffer, id=offer_id)
    requirements = get_object_or_404(ApplicationRequirements, job_offer__id=offer_id)

    if request.user.is_authenticated and offer.user == request.user:
        offerForm = JobOfferForm(request.POST or None, instance=offer)
        requirementsForm = ApplicationForm(request.POST or None, instance=requirements)
        if request.method == 'POST':
            if offerForm.is_valid() and requirementsForm.is_valid():
                offerForm.save()
                requirementsForm.save()
                return redirect('jobs:offer_detail', offer_id=offer_id)
            else:
                title = 'Invalid Data while updating fields.'

        context = {
            'offerForm': offerForm,
            'title': title,
            'requirements': requirementsForm,
        }
        return render(request, 'jobs/job_offer_add.html', context)

    return redirect('jobs:index')


# User Applications
@login_required
def user_applications(request, username):
    applications = []
    title = 'Your Applications'
    if request.user.is_authenticated:
        applications = JobApplication.objects.filter(user=request.user).order_by('-created_date')

    paginator = Paginator(applications, 10)
    page = request.GET.get('page')

    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)

    context = {
        'applications': applications,
        'title': title,
    }
    return render(request, 'jobs/user_applications.html', context)


# Candidates
@login_required
def candidates(request, username):
    applications = []
    title = 'Your Candidates'
    if request.user.is_authenticated:
        applications = JobApplication.objects.filter(job_offer__user=request.user).order_by('-created_date')

    paginator = Paginator(applications, 10)
    page = request.GET.get('page')

    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)

    context = {
        'applications': applications,
        'title': title,
    }
    return render(request, 'jobs/candidates.html', context)


# User Offers
@login_required
def user_offers(request, username):
    offers = []
    if request.user.is_authenticated:
        offers = JobOffer.objects.filter(user=request.user).order_by('-created_date')
        paginator = Paginator(offers, 10)
        page = request.GET.get('page')

        try:
            offers = paginator.page(page)
        except PageNotAnInteger:
            offers = paginator.page(1)
        except EmptyPage:
            offers = paginator.page(paginator.num_pages)

    return render(request, 'jobs/user_offers.html', {'offers': offers})

# Job Offers
def job_offers(request):
    offers = JobOffer.objects.all().order_by('-created_date')
    industries = JobOffer.INDUSTRY_TYPES
    paginator = Paginator(offers, 10)
    page = request.GET.get('page')

    try:
        offers = paginator.page(page)
    except PageNotAnInteger:
        offers = paginator.page(1)
    except EmptyPage:
        offers = paginator.page(paginator.num_pages)

    context = {
        'offers': offers,
        'industries': industries,
    }
    return render(request, 'jobs/offers.html', context)


# Add Job Offers
@login_required
def job_offer_add(request):
    title = ""
    if request.method == 'POST':
        offerForm = JobOfferForm(request.POST, request.FILES)
        requirementsForm = ApplicationForm(request.POST)
        if offerForm.is_valid() and requirementsForm.is_valid():
            job_offer = offerForm.save(commit=False)
            job_offer.user = request.user
            job_offer.save()

            requirements = requirementsForm.save(commit=False)
            requirements.job_offer = job_offer
            requirements.save()

            return redirect('jobs:index')

        else:
            title = 'Invalid Form'

    offerForm = JobOfferForm()
    requirementsForm = ApplicationForm()
    context = {
        'offerForm': offerForm,
        'title': title,
        'requirements': requirementsForm,
    }
    return render(request, 'jobs/job_offer_add.html', context)


# Offer Details
@login_required
def offer_detail(request, offer_id):
    offer = get_object_or_404(JobOffer, id=offer_id)
    requirements = offer.requirements.rstrip().split('-')
    requirements = filter(None, requirements)
    whatWeOffer = offer.whatWeOffer.rstrip().split('-')
    whatWeOffer = filter(None, whatWeOffer)
    jobDescription = offer.jobDescription.rstrip().split('-')
    jobDescription = filter(None, jobDescription)
    aboutUs = offer.aboutUs.splitlines()
    context = {
        'offer': offer,
        'requirements': requirements,
        'whatWeOffer': whatWeOffer,
        'jobDescription': jobDescription,
        'aboutUs': aboutUs,
    }
    return render(request, 'jobs/offer_detail.html', context)


# Apply Job
@login_required
def job_apply(request, offer_id):
    title = ""
    offer = get_object_or_404(JobOffer, id=offer_id)
    req = get_object_or_404(ApplicationRequirements, job_offer_id=offer_id)
    if request.method == 'POST':
        applyForm = JobApplyForm(request.POST, request.FILES, extra='')
        if applyForm.is_valid():
            apply_form = applyForm.save(commit=False)
            apply_form.user = request.user
            apply_form.job_offer = offer
            apply_form.save()

            return redirect('/profile/applications', username=request.user.username)
        else:
            title = 'Invalid Form'

    requirements = {
        'picture': req.formPicture,
        'age': req.formAge,
        'education': req.formEducation,
        'placeOfResidence': req.formPlaceOfResidence,
        'aboutYou': req.formAboutYou,
        'currentStatus': req.formCurrentStatus,
        'languages': req.formLanguages,
        'experience': req.formExperience,
        'hobby': req.formHobby
    }

    applyForm = JobApplyForm(extra=requirements)
    context = {
        'offer': offer,
        'applyForm': applyForm,
        'title': title,
        'requirements': requirements,
    }
    return render(request, 'jobs/apply_now.html', context)