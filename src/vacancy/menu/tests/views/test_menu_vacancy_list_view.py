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


class MenuVacancyListViewListViewTest(TestCase):
    """
    空室一覧メニュービューのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

        response = self.client.post(
            reverse('login'),
            {'username': 'yworks', 'password': 'guest1234', },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_get_menu_vacancy_list_view(self):
        url = reverse('menu_vacancy_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
