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


class DocumentsIndexViewTest(TestCase):
    """
    ドキュメント一覧ビューのテスト
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

        url = reverse('documents_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        document = response.context['documents'].first()
        self.assertEqual(document.file_title, '書類サンプル1')
