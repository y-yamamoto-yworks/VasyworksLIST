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


class AreaResidentialBuildingListViewTest(TestCase):
    """
    エリア建物リストビューのテスト
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

    def test_get_area_building_list_view(self):
        url = reverse(
            'building_area_building_list',
            args=['MjYwNDk'],       # 烏丸
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        building = response.context['buildings'][0]
        self.assertEqual(building.building_name, 'リストサンプルマンション1')

    def test_get_area_building_list_view_with_page(self):
        url = reverse(
            'building_area_building_list',
            args=[
                'MjYwNDk',      # 烏丸
                '2',
            ],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        building = response.context['buildings'][0]
        self.assertEqual(building.building_name, 'リストサンプルマンション11')
