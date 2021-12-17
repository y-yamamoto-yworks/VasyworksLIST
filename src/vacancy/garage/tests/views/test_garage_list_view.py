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


class GarageListViewTest(TestCase):
    """
    駐車場リストビューのテスト
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

    def test_get_garage_list_view(self):
        url = reverse('garage_garage_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        garage = response.context['garages'][0]
        self.assertEqual(garage.building_name, 'サンプルガレージ01')

    def test_get_garage_list_view_with_page(self):
        url = reverse(
            'garage_garage_list',
            args=['2'],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        garage = response.context['garages'][0]
        self.assertEqual(garage.building_name, 'サンプルガレージ14')

    def test_post_garage_list_view_with_garage_name(self):
        url = reverse('garage_garage_list')
        response = self.client.post(
            url,
            {
                'garage_name': 'ガレージ02',
                'pref': '26',
                'city': '0',
                'area': '0',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        garage = response.context['garages'][0]
        self.assertEqual(garage.building_name, 'サンプルガレージ02')

    def test_post_garage_list_view_with_area(self):
        url = reverse('garage_garage_list')
        response = self.client.post(
            url,
            {
                'garage_name': '',
                'pref': '26',
                'city': '26106',    # 京都市下京区
                'area': '26053',    # 京阪五条
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        garage = response.context['garages'][0]
        self.assertEqual(garage.building_name, 'サンプルガレージ01')

    def test_post_garage_list_view_with_city(self):
        url = reverse('garage_garage_list')
        response = self.client.post(
            url,
            {
                'garage_name': '',
                'pref': '26',
                'city': '26106',    # 京都市下京区
                'area': '0',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        garage = response.context['garages'][0]
        self.assertEqual(garage.building_name, 'サンプルガレージ01')
