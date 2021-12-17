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


class RoomMovieModelTest(TestCase):
    """
    部屋動画のテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.room = Room.objects.get(pk=3)      # 表示項目確認用マンション DEMO1号室
        self.movie = self.room.room_movies.first()

        if transaction.get_autocommit():
            transaction.set_autocommit(False)

    def tearDown(self):
        transaction.rollback()

    def test_room_movie_cache_file_url(self):
        self.room.building.auth_user = VacancyUser.objects.get(username='yworks')
        file_oid = '7112299ba5e743428e02a0824a3582d0'   # 表示項目確認用マンション
        cache_file_name = '240a825cd2c54494a830c188e1c6b8af.mp4'      # 室内
        self.assertEqual(
            self.movie.cache_file_url,
            '/viewer/cache_media/buildings/' + file_oid + '/' + cache_file_name,
        )
