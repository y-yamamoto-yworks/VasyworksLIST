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


class PrefViewSetTest(TestCase):
    """
    都道府県ビューセットのテスト
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

    def test_get_pref_view_set(self):
        url = reverse(
            'api_prefs',
        )
        response = self.client.get(url, HTTP_X_API_KEY=ApiHelper.get_key())
        self.assertEqual(response.status_code, 200)
        pref = response.data[0]
        self.assertEqual(pref['name'], '京都府')

        response_invalid = self.client.get(url, HTTP_X_API_KEY='AABBCCDDEEFF')
        self.assertEqual(response_invalid.status_code, 403)
