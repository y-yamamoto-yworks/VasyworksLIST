"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.db import transaction
from rent_db.models import Building
from rent_db.models import Pref, City, Area
from users.models import VacancyUser
import warnings


class BuildingModelTest(TestCase):
    """
    建物モデルのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.building = Building.objects.get(pk=2)      # 表示項目確認用マンション

        if transaction.get_autocommit():
            transaction.set_autocommit(False)

    def tearDown(self):
        transaction.rollback()

    def test_building_id_text(self):
        self.assertEqual(self.building.building_id_text, 'Y002')

    def test_building_vacancy_rooms(self):
        self.building.auth_user = VacancyUser.objects.get(username='yworks')
        room = self.building.vacancy_rooms.first()
        self.assertEqual(room.room_no, 'DEMO1')

    def test_building_facilities(self):
        facility = self.building.facilities.first()
        self.assertEqual(facility.facility_name, 'コンビニDEMO')

    def test_building_garages(self):
        garage = self.building.garages.first()
        self.assertEqual(garage.garage_name, 'DEMO01')

    def test_building_landmarks(self):
        landmark = self.building.landmarks.first()
        self.assertEqual(landmark.landmark.name, '京都府立大学')

    def test_building_files(self):
        file = self.building.files.first()
        self.assertEqual(file.file_title, '建物ファイルDEMO1')

    def test_building_movies(self):
        movie = self.building.movies.first()
        self.assertEqual(movie.movie_type.name, '屋内スペース')

    def test_building_panoramas(self):
        panorama = self.building.panoramas.first()
        self.assertEqual(panorama.panorama_type.name, 'エントランス')

    def test_building_pictures(self):
        picture = self.building.pictures.first()
        self.assertEqual(picture.picture_type.name, '建物外観')

    def test_building_address(self):
        self.assertEqual(self.building.address, '京都府京都市上京区住所町域DEMO町番地DEMOデータ A棟')
        self.building.building_no = None
        self.assertEqual(self.building.address, '京都府京都市上京区住所町域DEMO町番地DEMOデータ')

    def test_building_nearest_stations(self):
        self.assertEqual(self.building.nearest_station1, '地下鉄烏丸線 北大路 駅まで徒歩5分')
        self.building.station1_id = 0
        self.assertIsNone(self.building.nearest_station1)

        self.assertEqual(self.building.nearest_station2, '地下鉄烏丸線 鞍馬口 駅までバス10分（バス停 北大路バスターミナルまで徒歩5分）')
        self.building.station2_id = 0
        self.assertIsNone(self.building.nearest_station2)

        self.assertEqual(self.building.nearest_station3, '京福電鉄北野線 北野白梅町 駅までバス15分（バス停 北大路バスターミナルまで徒歩5分）')
        self.building.station3_id = 0
        self.assertIsNone(self.building.nearest_station3)

    def test_area_text(self):
        self.assertEqual(self.building.area_text, '今出川')

    def test_building_type_text(self):
        self.assertEqual(self.building.building_type_text, 'アパート（建物種別DEMOデータ）')

    def test_build_year_month(self):
        self.assertEqual(self.building.build_year_month, '1995年3月築')

    def test_structure_text(self):
        self.assertEqual(self.building.structure_text, '軽量鉄骨造（建物構造DEMOデータ）')

    def test_elementary_school_text(self):
        self.assertEqual(self.building.elementary_school_text, '新町')

    def test_elementary_school_distance_text(self):
        self.assertEqual(self.building.elementary_school_distance_text, '100 m')

    def test_junior_high_school_text(self):
        self.assertEqual(self.building.junior_high_school_text, '上京')

    def test_junior_high_school_distance_text(self):
        self.assertEqual(self.building.junior_high_school_distance_text, '200 m')

    def test_garage_status_text(self):
        self.assertIsNone(self.building.garage_status_text)
        old_type_id = self.building.garage_type_id
        self.building.garage_type_id = 1
        self.assertEqual(self.building.garage_status_text, '要確認')
        self.building.garage_type_id = old_type_id

    def test_garage_distance_text(self):
        self.assertEqual(self.building.garage_distance_text, '100 m')

    def test_garage_fee_text(self):
        self.assertIsNone(self.building.garage_fee_text)
        old_type_id = self.building.garage_type_id
        self.building.garage_type_id = 1
        self.building.garage_fee_lower = 12000
        self.building.garage_fee_upper = 15000
        self.building.garage_fee_tax_type_id = 1
        self.assertEqual(self.building.garage_fee_text, '12,000 円 〜 15,000 円 税別')
        self.building.garage_type_id = old_type_id

    def test_garage_charge_text(self):
        self.assertEqual(self.building.garage_charge_text, '4,000 円 〜 6,000 円 税別')

    def test_bike_parking_type_text(self):
        self.assertEqual(self.building.bike_parking_type_text, '原付可（有料）')

    def test_bike_parking_roof_text(self):
        self.assertEqual(self.building.bike_parking_roof_text, '屋根付き')

    def test_staff1_text(self):
        self.assertEqual(self.building.staff1_text, 'DEMO（賃貸管理部）')

    def test_staff2_text(self):
        self.assertEqual(self.building.staff2_text, '管理（賃貸管理部）')

    def test_register_text(self):
        self.assertEqual(self.building.register_text, '登記番号: 999番 / 登記地番: 登記所在地DEMO町999番地（家屋番号: 999番）')

    def test_agreement_existence_text(self):
        self.assertEqual(self.building.agreement_existence_text, '有り')

    def test_vacancy_recommend_comment(self):
        self.assertEqual(self.building.vacancy_recommend_comment, '空室情報キャッチコピーDEMOデータ')

    def test_search_with_city_id(self):
        building = Building.search_with_city_id(
            26101,      # 京都市北区
            VacancyUser.objects.get(username='yworks'),
            True,
            False,
        ).first()
        self.assertEqual(building.building_name, 'サンプルマンション')

    def test_search_with_city_id_only_non_residential(self):
        building = Building.search_with_city_id(
            26102,      # 京都市上京区
            VacancyUser.objects.get(username='yworks'),
            False,
            True,
        ).first()
        self.assertEqual(building.building_name, '表示項目確認用マンション')

    def test_search_with_area_id(self):
        building = Building.search_with_area_id(
            26004,      # 大宮
            VacancyUser.objects.get(username='yworks'),
            True,
            False,
        ).first()
        self.assertEqual(building.building_name, 'サンプルマンション')

    def test_search_with_building_name(self):
        building = Building.search_with_building_name(
            'サンプル',
            VacancyUser.objects.get(username='yworks'),
        ).first()
        self.assertEqual(building.building_name, 'サンプルマンション')

    def test_search_with_area_id_only_non_residential(self):
        building = Building.search_with_area_id(
            26018,      # 今出川
            VacancyUser.objects.get(username='yworks'),
            False,
            True,
        ).first()
        self.assertEqual(building.building_name, '表示項目確認用マンション')

    def test_search_non_residential_with_pref(self):
        building = Building.search_non_residential(
            VacancyUser.objects.get(username='yworks'),
            Pref.objects.get(pk=26),        # 京都
            None,
            None,
        ).first()
        self.assertEqual(building.building_name, '表示項目確認用マンション')

    def test_search_non_residential_with_city(self):
        building = Building.search_non_residential(
            VacancyUser.objects.get(username='yworks'),
            Pref.objects.get(pk=26),        # 京都
            City.objects.get(pk=26102),     # 京都市上京区
            None,
        ).first()
        self.assertEqual(building.building_name, '表示項目確認用マンション')

    def test_search_non_residential_with_area(self):
        building = Building.search_non_residential(
            VacancyUser.objects.get(username='yworks'),
            Pref.objects.get(pk=26),        # 京都
            City.objects.get(pk=26102),     # 京都市上京区
            Area.objects.get(pk=26018),     # 今出川
        ).first()
        self.assertEqual(building.building_name, '表示項目確認用マンション')

    def test_search_garage_with_pref(self):
        building = Building.search_garage(
            VacancyUser.objects.get(username='yworks'),
            None,
            Pref.objects.get(pk=26),        # 京都
            None,
            None,
        ).first()
        self.assertEqual(building.building_name, 'サンプルガレージ01')

    def test_search_garage_with_city(self):
        building = Building.search_garage(
            VacancyUser.objects.get(username='yworks'),
            None,
            Pref.objects.get(pk=26),        # 京都
            City.objects.get(pk=26106),     # 京都市下京区
            None,
        ).first()
        self.assertEqual(building.building_name, 'サンプルガレージ01')

    def test_search_garage_with_area(self):
        building = Building.search_garage(
            VacancyUser.objects.get(username='yworks'),
            None,
            Pref.objects.get(pk=26),        # 京都
            City.objects.get(pk=26106),     # 京都市下京区
            Area.objects.get(pk=26053),     # 京阪五条
        ).first()
        self.assertEqual(building.building_name, 'サンプルガレージ01')

    def test_search_garage_with_name(self):
        building = Building.search_garage(
            VacancyUser.objects.get(username='yworks'),
            'サンプルガレージ',
            None,
            None,
            None,
        ).first()
        self.assertEqual(building.building_name, 'サンプルガレージ01')

    def test_get_recommended_buildings(self):
        building = Building.get_recommended_buildings(
            VacancyUser.objects.get(username='yworks'),
        ).first()
        self.assertEqual(building.building_name, 'サンプルマンション')
