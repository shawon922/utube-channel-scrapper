from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

User = get_user_model()


class VideoListAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_videos_list(self):
        url = reverse('videos-api:list')
        client = self.client
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(status.is_success(response.status_code))
