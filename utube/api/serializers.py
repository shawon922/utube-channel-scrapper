from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from taggit.models import Tag

from utube.models import Channel, Video


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']
        ordering = ['-id']

    def to_representation(self, instance):
        return instance.name if instance else ''


class VideoListSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    channel_name = SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id',
            'channel',
            'channel_name',
            'tags',
            'video_uid',
            'title',
            'description',
            'published_at',
            'view_count',
            'comment_count',
            'like_count',
            'dislike_count',
            'favorite_count',
        ]
        ordering = ['-view_count']

    def get_channel_name(self, instance):
        if not instance.channel:
            return ''
        return instance.channel.title

    def get_tags(self, instance):
        if not instance.tags:
            return []

        tag_serializer = TagSerializer(instance.tags.all())

        return tag_serializer.data
