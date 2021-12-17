"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.db import transaction
from rent_db.models import VacancyTheme
from rent_db.models import Pref, City
from users.models import VacancyUser
import warnings


class VacancyThemeModelTest(TestCase):
    """
    空室情報テーマモデルのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')

        if transaction.get_autocommit():
            transaction.set_autocommit(False)

    def tearDown(self):
        transaction.rollback()

    def test_get_theme_rooms(self):
        theme = VacancyTheme.objects.get(pk=1)      # オススメ
        room = theme.get_theme_rooms(
            VacancyUser.objects.get(username='yworks'),
            Pref.objects.get(pk=26),  # 京都
            City.objects.get(pk=26102),  # 京都市上京区
            None,
        ).first()
        self.assertEqual(room.room_no, 'DEMO1')

    def test_get_themes(self):
        theme = VacancyTheme.get_themes(VacancyUser.objects.get(username='yworks')).first()
        self.assertEqual(theme.name, 'オススメ')
