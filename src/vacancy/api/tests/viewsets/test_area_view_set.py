"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.test import Client
from django.urls import reverse
import warnings
from api.api_helper import ApiHelper


class AreaViewSetTest(TestCase):
    """
    地域ビューセットのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

        response = self.client.post(
            reverse('login'),
            {'username': 'yworks', 'password': 'guest1234'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_get_area_view_set(self):
        url = reverse(
            'api_areas',
            args=[
                '26101',        # 京都市北区
            ],
        )
        response = self.client.get(url, HTTP_X_API_KEY=ApiHelper.get_key())
        self.assertEqual(response.status_code, 200)
        area = response.data[0]
        self.assertEqual(area['name'], '大北山')

        response_invalid = self.client.get(url, HTTP_X_API_KEY='AABBCCDDEEFF')
        self.assertEqual(response_invalid.status_code, 403)

