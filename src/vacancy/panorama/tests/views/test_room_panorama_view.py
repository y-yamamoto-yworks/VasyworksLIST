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


class RoomPanoramaViewTest(TestCase):
    """
    部屋パノラマビューのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

    def test_get_building_movie_view(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'yworks', 'password': 'guest1234', },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        url = reverse(
            'panorama_room_panorama',
            args=['MzU'],        # 表示項目確認用マンション DEMO1号室 居室（洋室）
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        panorama = response.context['panorama']
        self.assertEqual(panorama.panorama_type.name, '居室（洋室）')
