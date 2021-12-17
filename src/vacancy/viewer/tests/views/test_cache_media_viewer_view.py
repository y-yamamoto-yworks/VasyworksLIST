"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.test import Client
from django.urls import reverse
import warnings


class CacheMediaViewerViewTest(TestCase):
    """
    キャッシュメディアビューアビューのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

    def test_get_cache_media_viewer_view(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'yworks', 'password': 'guest1234', },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        url = reverse(
            'viewer_cache_media',
            args=['test_viewer/sample_picture.jpg'],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse(
            'viewer_cache_media',
            args=['test_viewer/sample_document.pdf'],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse(
            'viewer_cache_media',
            args=['test_viewer/sample_movie.mp4'],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse(
            'viewer_cache_media',
            args=['test_viewer/abcd.jpg'],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_cache_media_viewer_view_without_login(self):
        url = reverse(
            'viewer_cache_media',
            args=['test_viewer/sample_picture.jpg'],
        )
        response = self.client.get(url)
        self.assertRegex(response.url, '^/login/')
