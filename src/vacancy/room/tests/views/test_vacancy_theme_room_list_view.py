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


class VacancyThemeRoomListViewTest(TestCase):
    """
    空室情報テーマ部屋リストビューのテスト
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

    def test_get_vacancy_theme_room_list_view(self):
        url = reverse(
            'room_vacancy_theme_room_list',
            args=['MQ'],     # オススメ
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        room = response.context['rooms'][0]
        self.assertEqual(room.building.building_name, '表示項目確認用マンション')
        self.assertEqual(room.room_no, 'DEMO1')

    def test_post_vacancy_theme_room_list_view(self):
        url = reverse(
            'room_vacancy_theme_room_list',
            args=['MQ'],     # オススメ
        )
        response = self.client.post(
            url,
            {
                'pref': '26',
                'city': '26104',    # 京都市中京区
                'area': '26049',    # 烏丸
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        room = response.context['rooms'][0]
        self.assertEqual(room.building.building_name, 'リストサンプルマンション1')
        self.assertEqual(room.room_no, '101')

    def test_post_vacancy_theme_room_list_view_without_area(self):
        url = reverse(
            'room_vacancy_theme_room_list',
            args=['MQ'],     # オススメ
        )
        response = self.client.post(
            url,
            {
                'pref': '26',
                'city': '26104',    # 京都市中京区
                'area': '0',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        room = response.context['rooms'][0]
        self.assertEqual(room.building.building_name, 'リストサンプルマンション1')
        self.assertEqual(room.room_no, '101')
