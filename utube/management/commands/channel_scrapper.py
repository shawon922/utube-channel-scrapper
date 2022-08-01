import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from utube.scrapper.api import Api

from utube.models import Channel, Video

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(args, options)
        return
        api_key = settings.YOUTUBE_API_KEY
        api = Api(api_key=api_key)
        channel_ids = 'UChTsiSbpTuSrdOHpXkKlq6Q'
        channel_info = api.get_channel_info(channel_id=channel_ids, parts='snippet,statistics')

        channel_items = channel_info.get('items')

        if channel_items:
            for channel_item in channel_items:
                channel_id = channel_item.get('id')
                if not channel_id:
                    continue

                channel_snippet = channel_item.get('snippet')
                channel_statistics = channel_item.get('statistics')
                channel_instances = Channel.objects.filter(channel_uid=channel_id)

                if channel_instances.exists():
                    channel_instance = channel_instances.first()
                else:
                    channel_instance = Channel(channel_uid=channel_id)

                channel_instance.title = channel_snippet.get('title')
                channel_instance.description = channel_snippet.get('description')
                channel_instance.view_count = channel_statistics.get('viewCount')
                channel_instance.comment_count = channel_statistics.get('commentCount')
                channel_instance.subscriber_count = channel_statistics.get('subscriberCount')
                channel_instance.video_count = channel_statistics.get('videoCount')
                channel_instance.save()

                playlist_info = api.get_playlists(
                    channel_id=channel_id,
                    count=None,
                    limit=50,
                )

                playlists = playlist_info.get('items')
                playlist_item_ids = None

                if playlists:
                    playlist_item_ids = []
                    for playlist in playlists:
                        playlist_id = playlist.get('id')

                        if playlist_id:
                            playlist_items_info = api.get_playlist_items(
                                playlist_id=playlist_id,
                                parts='snippet,contentDetails',
                                count=None,
                                limit=50,
                            )
                            playlist_items = playlist_items_info.get('items')

                            if playlist_items:
                                for playlist_item in playlist_items:
                                    content_details = playlist_item.get('contentDetails')
                                    if content_details:
                                        playlist_item_ids.append(content_details.get('videoId'))

                                    if len(playlist_item_ids) == 50:
                                        self.save_videos(api, channel_instance, playlist_item_ids)

                                        playlist_item_ids = []

                if playlist_item_ids:
                    self.save_videos(api, channel_instance, playlist_item_ids)

    def save_videos(self, api, channel_instance, playlist_item_ids):
        video_info = api.get_video_by_id(
            video_id=playlist_item_ids,
            parts='snippet,statistics',
            limit=50,
        )

        video_items = video_info.get('items')
        if video_items:
            for video_item in video_items:
                video_snippet = video_item.get('snippet')
                video_statistics = video_item.get('statistics')
                video_tags = video_snippet.get('tags')
                video_id = video_item.get('id')
                video_instances = Video.objects.filter(video_uid=video_id)

                if video_instances.exists():
                    video_instance = video_instances.first()

                else:
                    video_instance = Video(video_uid=video_id)

                video_instance.channel = channel_instance
                video_instance.title = video_snippet.get('title')
                video_instance.description = video_snippet.get('description')
                video_instance.published_at = video_snippet.get('publishedAt')
                video_instance.view_count = video_statistics.get('viewCount')
                video_instance.comment_count = video_statistics.get('commentCount')
                video_instance.like_count = video_statistics.get('likeCount')
                video_instance.dislike_count = video_statistics.get('dislikeCount')
                video_instance.favorite_count = video_statistics.get('favoriteCount')
                video_instance.save()

                video_instance.tags.clear()
                if video_tags:
                    video_instance.tags.add(*video_tags)

