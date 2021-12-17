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


class BuildingGarageListViewTest(TestCase):
    """
    建物駐車場一覧ビューのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

    def test_get_building_garage_list_view(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'yworks', 'password': 'guest1234', },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        url = reverse(
            'building_garage_list',
            args=['98d6c2ccd9384062ab5fb4dd61b3e8fc'],        # 表示項目確認用マンション
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        building = response.context['building']
        garage = building.garages.first()
        self.assertEqual(garage.garage_name, 'DEMO01')
