from django.db.models import Q

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.permissions import (
    AllowAny,
)

from utube.models import Video

from .pagination import (
    VideoPageNumberPagination,
)

from .serializers import VideoListSerializer


class VideoListAPIView(ListAPIView):
    """
    List:
    Return a list of all the existing videos.
    """
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['description', 'title']
    serializer_class = VideoListSerializer
    pagination_class = VideoPageNumberPagination # VideoLimitOffsetPagination # PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Video.objects.all()
        title = self.request.GET.get('title')
        tags = self.request.GET.get('tags')

        if title:
            queryset_list = queryset_list.filter(title__icontains=title)
        
        if tags:
            queryset_list = queryset_list.filter(tags__name__icontains=tags)
        
        query = self.request.GET.get('search')
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()

        return queryset_list

