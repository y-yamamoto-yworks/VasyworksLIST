"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.db import transaction
from rent_db.models import Building
from users.models import VacancyUser
import warnings


class BuildingMovieModelTest(TestCase):
    """
    建物動画のテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.building = Building.objects.get(pk=2)      # 表示項目確認用マンション
        self.movie = self.building.building_movies.first()

        if transaction.get_autocommit():
            transaction.set_autocommit(False)

    def tearDown(self):
        transaction.rollback()

    def test_building_movie_cache_file_url(self):
        self.building.auth_user = VacancyUser.objects.get(username='yworks')
        file_oid = '7112299ba5e743428e02a0824a3582d0'   # 表示項目確認用マンション
        cache_file_name = '1bae955702b9426a8a0cb73152c7abe2.mp4'      # 屋内スペース
        self.assertEqual(
            self.movie.cache_file_url,
            '/viewer/cache_media/buildings/' + file_oid + '/' + cache_file_name,
        )
