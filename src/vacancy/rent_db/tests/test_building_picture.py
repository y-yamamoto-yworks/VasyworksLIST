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


class BuildingPictureModelTest(TestCase):
    """
    建物画像のテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.building = Building.objects.get(pk=2)      # 表示項目確認用マンション
        self.picture = self.building.building_pictures.first()

        if transaction.get_autocommit():
            transaction.set_autocommit(False)

    def tearDown(self):
        transaction.rollback()

    def test_building_picture_thumbnail_file_url(self):
        self.building.auth_user = VacancyUser.objects.get(username='yworks')
        file_oid = '7112299ba5e743428e02a0824a3582d0'   # 表示項目確認用マンション
        cache_file_name = 'ae4499eed2c94f828cd0e37aec938558.JPG'      # 建物外観
        self.assertEqual(
            self.picture.thumbnail_file_url,
            '/viewer/cache_media/buildings/' + file_oid + '/' + cache_file_name,
        )

    def test_building_picture_cache_file_url(self):
        self.building.auth_user = VacancyUser.objects.get(username='yworks')
        file_oid = '7112299ba5e743428e02a0824a3582d0'   # 表示項目確認用マンション
        cache_file_name = 'c747648e79004f07ae10079898cc6faf.JPG'      # 建物外観
        self.assertEqual(
            self.picture.cache_file_url,
            '/viewer/cache_media/buildings/' + file_oid + '/' + cache_file_name,
        )
