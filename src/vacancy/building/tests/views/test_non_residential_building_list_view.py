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


class NonResidentialBuildingListViewTest(TestCase):
    """
    非居住建物リストビューのテスト
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

    def test_get_non_residential_building_list_view(self):
        url = reverse('building_non_residential_building_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        building = response.context['buildings'][0]
        self.assertEqual(building.building_name, '表示項目確認用マンション')

    def test_get_non_residential_building_list_view_with_page(self):
        url = reverse(
            'building_non_residential_building_list',
            args=['2'],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        building = response.context['buildings'][0]
        self.assertEqual(building.building_name, 'サンプルテナントビル10')

    def test_post_non_residential_building_list_view(self):
        url = reverse('building_non_residential_building_list')
        response = self.client.post(
            url,
            {
                'pref': '26',
                'city': '26105',    # 京都市東山区
                'area': '26051',    # 祇園
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        building = response.context['buildings'][0]
        self.assertEqual(building.building_name, 'サンプルテナントビル01')

    def test_post_non_residential_building_list_view_without_area(self):
        url = reverse('building_non_residential_building_list')
        response = self.client.post(
            url,
            {
                'pref': '26',
                'city': '26105',    # 京都市東山区
                'area': '0',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        building = response.context['buildings'][0]
        self.assertEqual(building.building_name, 'サンプルテナントビル01')
