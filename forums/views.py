#Import Dependencies
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, UpdateView, DeleteView
from .forms import NewTopicForm, PostForm
from .models import Board, Post, Topic

#Views

#View function for Board List
class BoardListView(ListView):
    template_name = 'forums/home.html'
    model = Board

#View function for Updating Post
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'forums/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

#View function for list of topics
class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'forums/board_topics.html'
    paginate_by = 5

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context

#View function for list of posts
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'forums/topic_posts.html'
    paginate_by = 2

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        context = super().get_context_data(**kwargs)
        context['topic'] = self.topic
        return context

#View Function for new post
@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = request.user

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user,
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()

    context = {'board': board, 'form': form}
    return render(request, 'forums/new_topic.html', context)

#View function for replying to topics
@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    posts = topic.posts.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    context = {'topic': topic, 'posts': posts, 'form': form}
    return render(request, 'forums/reply_topic.html', context)
