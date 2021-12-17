"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.db import transaction
from django.conf import settings
from rent_db.models import Room
from users.models import VacancyUser
import warnings


class RoomModelTest(TestCase):
    """
    部屋モデルのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.room = Room.objects.get(pk=3)      # 表示項目確認用マンション DEMO1号室

        if transaction.get_autocommit():
            transaction.set_autocommit(False)

    def tearDown(self):
        transaction.rollback()

    def test_room_equipments(self):
        room_equipment = self.room.equipments.first()
        self.assertEqual(room_equipment.equipment.name, '2口コンロ付')

    def test_room_movies(self):
        movie = self.room.movies.first()
        self.assertEqual(movie.movie_type.name, '室内')

    def test_room_panoramas(self):
        panorama = self.room.panoramas.first()
        self.assertEqual(panorama.panorama_type.name, '居室（洋室）')

    def test_room_pictures(self):
        picture = self.room.pictures.first()
        self.assertEqual(picture.picture_type.name, '間取図')

    def test_is_no_publish(self):
        self.assertFalse(self.room.is_no_publish)

        old_is_no_publish = self.room.is_no_publish
        self.room.is_publish_vacancy = False
        self.assertTrue(self.room.is_no_publish)
        self.room.is_publish_vacancy = old_is_no_publish

        old_start_date = self.room.vacancy_start_date
        self.room.vacancy_start_date = '2999-12-31'
        self.assertTrue(self.room.is_no_publish)
        self.room.vacancy_start_date = old_start_date

        old_end_date = self.room.vacancy_end_date
        self.room.vacancy_end_date = '2000-01-01'
        self.assertTrue(self.room.is_no_publish)
        self.room.vacancy_end_date = old_end_date

    def test_is_high_auth_level(self):
        self.assertFalse(self.room.is_high_auth_level)
        self.room.room_auth_level_id = settings.STANDARD_AUTH_LEVEL + 1
        self.assertTrue(self.room.is_high_auth_level)

    def test_room_floor_text(self):
        self.assertEqual(self.room.room_floor_text, '1階')

    def test_rent_text(self):
        self.assertEqual(self.room.rent_text, '52,000 円')

        old_rent = self.room.rent
        self.room.rent = 0
        self.assertIsNone(self.room.rent_text)
        self.room.rent = old_rent

        old_tax_id = self.room.rent_tax_type_id
        self.room.rent_tax_type_id = 1
        self.assertEqual(self.room.rent_text, '52,000 円（税別）')
        self.room.rent_tax_type_id = 3
        self.assertEqual(self.room.rent_text, '52,000 円')
        self.room.rent_tax_type_id = old_tax_id

        old_rent_hidden = self.room.rent_hidden
        self.room.rent_hidden = True
        self.assertEqual(self.room.rent_text, '相談')
        self.room.rent_hidden = old_rent_hidden

    def test_rent_upper_text(self):
        self.assertEqual(self.room.rent_upper_text, '53,000 円')

        old_rent_upper = self.room.rent_upper
        self.room.rent_upper = 0
        self.assertIsNone(self.room.rent_upper_text)
        self.room.rent_upper = self.room.rent
        self.assertIsNone(self.room.rent_upper_text)
        self.room.rent_upper = old_rent_upper

        old_tax_id = self.room.rent_tax_type_id
        self.room.rent_tax_type_id = 1
        self.assertEqual(self.room.rent_upper_text, '53,000 円（税別）')
        self.room.rent_tax_type_id = 3
        self.assertEqual(self.room.rent_upper_text, '53,000 円')
        self.room.rent_tax_type_id = old_tax_id

        old_rent_hidden = self.room.rent_hidden
        self.room.rent_hidden = True
        self.assertIsNone(self.room.rent_upper_text)
        self.room.rent_hidden = old_rent_hidden

    def test_trader_rent_text(self):
        self.assertEqual(self.room.trader_rent_text, '55,000 円')

        old_trader_rent = self.room.trader_rent
        self.room.trader_rent = 0
        self.assertIsNone(self.room.trader_rent_text)
        self.room.trader_rent = old_trader_rent

        old_tax_id = self.room.rent_tax_type_id
        self.room.rent_tax_type_id = 1
        self.assertEqual(self.room.trader_rent_text, '55,000 円（税別）')
        self.room.rent_tax_type_id = 3
        self.assertEqual(self.room.trader_rent_text, '55,000 円')
        self.room.rent_tax_type_id = old_tax_id

    def test_condo_fees_text(self):
        self.assertEqual(self.room.condo_fees_text, '3,000 円')
        self.room.condo_fees_type_id = 20
        self.assertEqual(self.room.condo_fees_text, '込み')

    def test_water_cost_text(self):
        self.assertEqual(self.room.water_cost_text, '2,000 円（税込）')
        self.room.water_cost_type_id = 30
        self.assertEqual(self.room.water_cost_text, '共益費込')

    def test_water_check_text(self):
        self.assertEqual(self.room.water_check_text, '管理会社')

    def test_payment_type_text(self):
        self.assertEqual(self.room.payment_type_text, '振替')

    def test_payment_fee_type_text(self):
        self.assertEqual(self.room.payment_fee_type_text, '振替手数料')

    def test_payment_fee_text(self):
        self.assertEqual(self.room.payment_fee_text, ' 300 円（税別）')

    def test_free_rent_text(self):
        self.assertEqual(self.room.free_rent_text, '1ヶ月')
        self.room.free_rent_type_id = 2
        self.room.free_rent_limit_year = 2021
        self.room.free_rent_limit_month = 5
        self.assertEqual(self.room.free_rent_text, '2021年5月まで')
        self.room.free_rent_type_id = 0
        self.assertIsNone(self.room.free_rent_text)

    def test_room_monthly_cost_texts(self):
        self.assertEqual(self.room.monthly_cost_text1, '1,000 円(税別)')
        self.assertEqual(self.room.monthly_cost_text2, '500 円(税込)')
        self.assertEqual(self.room.monthly_cost_text3, '2,000 円(税別)')
        self.assertIsNone(self.room.monthly_cost_text4)
        self.assertIsNone(self.room.monthly_cost_text5)
        self.assertIsNone(self.room.monthly_cost_text6)
        self.assertIsNone(self.room.monthly_cost_text7)
        self.assertIsNone(self.room.monthly_cost_text8)
        self.assertIsNone(self.room.monthly_cost_text9)
        self.assertIsNone(self.room.monthly_cost_text10)

    def test_room_deposit_texts(self):
        self.room.deposit_notation1_id = 1
        self.assertEqual(self.room.deposit_text1, '無し')
        self.room.deposit_notation1_id = 2
        self.room.deposit_value1 = 100000
        self.assertEqual(self.room.deposit_text1, '100,000 円')

        self.assertIsNone(self.room.deposit_text2)
        self.room.deposit_type2_id = 20
        self.room.deposit_notation2_id = 1
        self.assertEqual(self.room.deposit_text2, '無し')
        self.room.deposit_notation2_id = 2
        self.room.deposit_value2 = 100000
        self.assertEqual(self.room.deposit_text2, '100,000 円')

    def test_room_key_money_texts(self):
        self.assertEqual(self.room.key_money_text1, '賃料 1 ヶ月')
        self.room.key_money_notation1_id = 1
        self.assertEqual(self.room.key_money_text1, '無し')
        self.room.key_money_notation1_id = 2
        self.room.key_money_value1 = 100000
        self.assertEqual(self.room.key_money_text1, '100,000 円')

        self.assertIsNone(self.room.key_money_text2)
        self.room.key_money_type2_id = 20
        self.room.key_money_notation2_id = 1
        self.assertEqual(self.room.key_money_text2, '無し')
        self.room.key_money_notation2_id = 2
        self.room.key_money_value2 = 100000
        self.assertEqual(self.room.key_money_text2, '100,000 円')

    def test_room_insurance_type_text(self):
        self.assertEqual(self.room.insurance_type_text, '指定')

    def test_room_insurance_company_text(self):
        self.assertEqual(self.room.insurance_company_text, '部屋火災保険会社DEMO')

    def test_room_insurance_text(self):
        self.assertEqual(self.room.insurance_text, '2年15,000 円（税込）')
        self.room.insurance_type_id = 3
        self.assertIsNone(self.room.insurance_text)

    def test_guarantee_type_text(self):
        self.assertEqual(self.room.guarantee_type_text, '必須')

    def test_room_document_cost_text(self):
        self.assertEqual(self.room.document_cost_text, '8,000 円（税込）')
        self.room.document_cost_existence_id = 2
        self.assertIsNone(self.room.document_cost_text)

    def test_room_key_change_cost_text(self):
        self.assertEqual(self.room.key_change_cost_text, '15,000 円（税別）')
        self.room.key_change_cost_existence_id = 2
        self.assertEqual(self.room.key_change_cost_text, None)

    def test_room_initial_cost_texts(self):
        self.assertEqual(self.room.initial_cost_text1, '5,000 円(税別)')
        self.assertEqual(self.room.initial_cost_text2, '10,000 円(税別)')
        self.assertEqual(self.room.initial_cost_text3, '500 円(税別)')
        self.assertIsNone(self.room.initial_cost_text4)
        self.assertIsNone(self.room.initial_cost_text5)
        self.assertIsNone(self.room.initial_cost_text6)
        self.assertIsNone(self.room.initial_cost_text7)
        self.assertIsNone(self.room.initial_cost_text8)
        self.assertIsNone(self.room.initial_cost_text9)
        self.assertIsNone(self.room.initial_cost_text10)

    def test_room_contract_span_text(self):
        building = self.room.building  # 表示項目確認用マンション
        room = building.rooms.first()
        self.assertEqual(room.contract_span_text, '2年')
        room.contract_years = 0
        room.contract_months = 0
        self.assertIsNone(room.contract_span_text)
        room.contract_months = 10
        self.assertEqual(room.contract_span_text, '10ヶ月')
        room.contract_years = 1
        room.contract_months = 6
        self.assertEqual(room.contract_span_text, '1年6ヶ月')

    def test_room_renewal_fee_text(self):
        self.assertEqual(self.room.renewal_fee_text, '新賃料の 1 ヶ月')
        self.room.renewal_fee_notation_id = 1
        self.assertEqual(self.room.renewal_fee_text, '無し')
        self.room.renewal_fee_notation_id = 2
        self.room.renewal_fee_value = 50000
        self.assertEqual(self.room.renewal_fee_text, '50,000 円')

    def test_room_renewal_charge_text(self):
        self.assertEqual(self.room.renewal_charge_text, '10,000 円（税別）')
        self.room.renewal_charge_existence_id = 2
        self.assertIsNone(self.room.renewal_charge_text)

    def test_room_recontract_fee_text(self):
        self.assertIsNone(self.room.recontract_fee_text)
        self.room.recontract_fee_existence_id = 1
        self.room.recontract_fee = 33000
        self.room.recontract_fee_tax_type_id = 2
        self.assertEqual(self.room.recontract_fee_text, '33,000 円（税込）')

    def test_room_cancel_notice_limit_text(self):
        self.assertEqual(self.room.cancel_notice_limit_text, '2ヶ月前')
        self.room.cancel_notice_limit = 0
        self.assertIsNone(self.room.cancel_notice_limit_text)

    def test_room_cleaning_cost_text(self):
        self.assertEqual(self.room.cleaning_cost_text, '敷金相殺15,000 円（税別）')
        self.room.cleaning_type_id = 1
        self.assertIsNone(self.room.cleaning_cost_text)

    def test_room_area_texts(self):
        self.assertEqual(self.room.room_area_text, '40.55')
        self.assertEqual(self.room.balcony_area_text, '7')

    def test_room_balcony_type_text(self):
        self.assertEqual(self.room.balcony_type_text, 'ベランダ')

    def test_room_layout_type_text(self):
        self.assertEqual(self.room.layout_type_text, '3DK')

    def test_room_layout_detail_text(self):
        self.assertEqual(self.room.layout_detail_text, '洋6帖×和6帖×DK4.5帖')

    def test_room_direction_text(self):
        self.assertEqual(self.room.direction_text, '南')

    def test_room_ad_text(self):
        self.assertEqual(self.room.ad_text, '賃料の 1 ヶ月（税別）')
        self.room.ad_type_id = 2
        self.room.ad_value = 55000
        self.room.ad_tax_type_id = 2
        self.assertEqual(self.room.ad_text, '55,000 円（税込）')
        self.room.ad_type_id = 1
        self.assertEqual(self.room.ad_text, '無し')
        self.room.ad_type_id = 0
        self.assertIsNone(self.room.ad_text)

    def test_room_trader_ad_text(self):
        self.assertIsNone(self.room.trader_ad_text)
        self.room.trader_ad_type_id = 3
        self.room.trader_ad_value = 0.5
        self.room.trader_ad_tax_type_id = 1
        self.assertEqual(self.room.trader_ad_text, '賃料の 0.5 ヶ月（税別）')
        self.room.trader_ad_type_id = 2
        self.room.trader_ad_value = 44000
        self.room.trader_ad_tax_type_id = 2
        self.assertEqual(self.room.trader_ad_text, '44,000 円（税込）')
        self.room.trader_ad_type_id = 1
        self.assertEqual(self.room.trader_ad_text, '無し')
        self.room.trader_ad_type_id = 0
        self.assertIsNone(self.room.trader_ad_text)

    def test_room_owner_fee_text(self):
        self.assertEqual(self.room.owner_fee_text, '有り（ADと別）')

    def test_room_vacancy_status_text(self):
        self.assertEqual(self.room.vacancy_status_text, '空き予定')

    def test_room_live_start_date_text(self):
        self.assertIsNone(self.room.live_start_date_text)
        old_status_id = self.room.room_status_id
        self.room.room_status_id = 4
        self.room.live_start_year = 2999
        self.room.live_start_month = 4
        self.room.live_start_day_id = 102
        self.assertEqual(self.room.live_start_date_text, '2999年4月上旬')
        self.room.room_status_id = old_status_id

    def test_room_cancel_scheduled_date_text(self):
        self.assertIsNone(self.room.cancel_scheduled_date_text)
        old_status_id = self.room.room_status_id
        self.room.room_status_id = 4
        self.room.cancel_scheduled_year = 2999
        self.room.cancel_scheduled_month = 3
        self.room.cancel_scheduled_day_id = 103
        self.assertEqual(self.room.cancel_scheduled_date_text, '2999年3月中旬')
        self.room.room_status_id = old_status_id

    def test_room_electric_text(self):
        self.assertEqual(self.room.electric_text, '関西電力')

    def test_room_gas_text(self):
        self.assertEqual(self.room.gas_text, '都市ガス')

    def test_room_bath_text(self):
        self.assertEqual(self.room.bath_text, 'バストイレ別')

    def test_room_toilet_text(self):
        self.assertEqual(self.room.toilet_text, '洋式')

    def test_room_kitchen_range_text(self):
        self.assertEqual(self.room.kitchen_range_text, 'ガスキッチン')

    def test_room_internet_text(self):
        self.assertEqual(self.room.internet_text, 'インターネット無料')

    def test_room_washer_text(self):
        self.assertEqual(self.room.washer_text, '室内設置可')

    def test_room_pet_text(self):
        self.assertEqual(self.room.pet_text, '犬猫可')

    def test_room_reform_year_month(self):
        self.assertEqual(self.room.reform_year_month, '2020年9月')
        self.room.reform_year = 0
        self.assertIsNone(self.room.reform_year_month)

    def test_room_trader_publish_text(self):
        self.assertEqual(self.room.trader_publish_text, '可')

    def test_room_trader_portal_text(self):
        self.assertEqual(self.room.trader_portal_text, '不可')

    def test_room_vacancy_theme_appeal_text(self):
        self.assertEqual(self.room.vacancy_theme_appeal_text, '部屋空室情報アピールDEMOデータ')
        self.room.vacancy_appeal = None
        self.assertEqual(self.room.vacancy_theme_appeal_text, '空室情報アピールDEMOデータ')

    def test_room_vacancy_theme_catch_copy_text(self):
        self.assertEqual(self.room.vacancy_theme_catch_copy_text, '部屋空室情報キャッチコピーDEMOデータ')
        self.room.vacancy_catch_copy = None
        self.assertEqual(self.room.vacancy_theme_catch_copy_text, '空室情報キャッチコピーDEMOデータ')

    def test_get_vacancy_room_condition_with_company_user(self):
        auth_user = VacancyUser.objects.get(username='yworks')
        query = Room.get_vacancy_room_condition(auth_user, True, False)
        rooms = self.room.building.rooms.filter(query).all()
        self.assertEqual(len(rooms), 4)
        query = Room.get_vacancy_room_condition(auth_user, True, True)
        rooms = self.room.building.rooms.filter(query).all()
        self.assertEqual(len(rooms), 5)
        query = Room.get_vacancy_room_condition(auth_user, False, True)
        rooms = self.room.building.rooms.filter(query).all()
        self.assertEqual(len(rooms), 1)

    def test_get_vacancy_room_condition_with_trader_user(self):
        auth_user = VacancyUser.objects.get(username='a-pool')
        query = Room.get_vacancy_room_condition(auth_user, True, False)
        rooms = self.room.building.rooms.filter(query).all()
        self.assertEqual(len(rooms), 3)
