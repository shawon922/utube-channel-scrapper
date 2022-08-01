from django.db import models
from taggit.managers import TaggableManager


class Channel(models.Model):
    channel_uid = models.CharField(max_length=100)
    title = models.CharField(max_length=255, null=True, blank=True, default=None)
    description = models.TextField(null=True, blank=True, default=None)
    view_count = models.PositiveIntegerField(null=True, blank=True, default=0)
    comment_count = models.PositiveIntegerField(null=True, blank=True, default=0)
    subscriber_count = models.PositiveIntegerField(null=True, blank=True, default=0)
    video_count = models.PositiveIntegerField(null=True, blank=True, default=0)


class Video(models.Model):
    channel = models.ForeignKey('Channel', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    tags = TaggableManager()
    video_uid = models.CharField(max_length=100)
    title = models.CharField(max_length=255, null=True, default=None)
    description = models.TextField(null=True, default=None)
    published_at = models.DateTimeField()
    view_count = models.PositiveIntegerField(null=True, blank=True, default=0)
    comment_count = models.PositiveIntegerField(null=True, blank=True, default=0)
    like_count = models.PositiveIntegerField(null=True, blank=True, default=0)
    dislike_count = models.PositiveIntegerField(null=True, blank=True, default=0)
    favorite_count = models.PositiveIntegerField(null=True, blank=True, default=0)

