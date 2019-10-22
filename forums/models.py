#Import Dependencies
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import Truncator

#Class for Board Table
class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('board_topics', args=[self.pk])

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

#Class for Topic Table
class Topic(models.Model):
    subject = models.CharField(max_length=256)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='topics',
    )
    starter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='topics',
    )
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('topic_posts', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.pk
        })

#Class for Post Table
class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='+',
    )

    def __str__(self):
        truncated = Truncator(self.message)
        return truncated.chars(30)
