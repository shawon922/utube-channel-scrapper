from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)


class VideoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10


class VideoPageNumberPagination(PageNumberPagination):
    page_size = 20
