"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.db import transaction
from rent_db.models import Room
from users.models import VacancyUser
import warnings


class RoomPictureModelTest(TestCase):
    """
    部屋画像のテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.room = Room.objects.get(pk=3)      # 表示項目確認用マンション DEMO1号室
        self.picture = self.room.room_pictures.first()

        if transaction.get_autocommit():
            transaction.set_autocommit(False)

    def tearDown(self):
        transaction.rollback()

    def test_room_picture_cache_file_url(self):
        self.room.building.auth_user = VacancyUser.objects.get(username='yworks')
        file_oid = '7112299ba5e743428e02a0824a3582d0'   # 表示項目確認用マンション
        cache_file_name = 'afb0f1d5d38c4c72926cbcde56476281.jpg'      # 間取図
        self.assertEqual(
            self.picture.cache_file_url,
            '/viewer/cache_media/buildings/' + file_oid + '/' + cache_file_name,
        )
