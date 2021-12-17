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


class SearchNameBuildingListViewTest(TestCase):
    """
    名称検索建物リストビューのテスト
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

    def test_get_search_name_building_list_view(self):
        url = reverse('building_search_name_building_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_get_search_name_building_list_view_with_page(self):
        url = reverse(
            'building_search_name_building_list',
            args=['2'],
        )
        url += '?name=%E3%83%9E%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%B3'    # 「マンション」で検索
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        building = response.context['buildings'][0]
        self.assertEqual(building.building_name, 'リストサンプルマンション7')

    def test_post_search_name_building_list_view(self):
        url = reverse('building_search_name_building_list')
        response = self.client.post(
            url,
            {
                'building_name': 'マンション',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        building = response.context['buildings'][0]
        self.assertEqual(building.building_name, 'サンプルマンション')
