from django.urls import path

from .views import (
    VideoListAPIView,
)

app_name = 'courses'

urlpatterns = [
    path('', VideoListAPIView.as_view(), name='list'),
]
