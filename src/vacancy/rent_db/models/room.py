"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from lib.convert import *
from lib.functions import *
from .ad_type import AdType
from .allow_type import AllowType
from .balcony_type import BalconyType
from .bath_type import BathType
from .cleaning_type import CleaningType
from .condo_fees_type import CondoFeesType
from .deposit_notation import DepositNotation
from .deposit_type import DepositType
from .direction import Direction
from .electric_type import ElectricType
from .existence import Existence
from .free_rent_type import FreeRentType
from .gas_type import GasType
from .guarantee_type import GuaranteeType
from .insurance_type import InsuranceType
from .internet_type import InternetType
from .key_money_notation import KeyMoneyNotation
from .key_money_type import KeyMoneyType
from .kitchen_type import KitchenType
from .kitchen_range_type import KitchenRangeType
from .layout_type import LayoutType
from .month_day import MonthDay
from .owner import Owner
from .owner_fee_type import OwnerFeeType
from .payment_fee_type import PaymentFeeType
from .payment_type import PaymentType
from .pet_type import PetType
from .renewal_fee_notation import RenewalFeeNotation
from .rental_type import RentalType
from .room_auth_level import RoomAuthLevel
from .room_status import RoomStatus
from .tax_type import TaxType
from .toilet_type import ToiletType
from .trader import Trader
from .vacancy_status import VacancyStatus
from .washer_type import WasherType
from .water_check_type import WaterCheckType
from .water_cost_type import WaterCostType
from users.models import VacancyUser


class Room(models.Model):
    """
    部屋
    """
    id = models.AutoField(_('id'), db_column='id', primary_key=True)

    oid = models.CharField(_('oid'), db_column='oid', db_index=True, unique=True, max_length=50)
    building = models.ForeignKey(
        'Building',
        db_column='building_id',
        related_name='rooms',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )

    room_no = models.CharField(_('room_no'), db_column='room_no', max_length=20, db_index=True, null=True, blank=True)
    room_floor = models.IntegerField(_('room_floor'), db_column='room_floor', default=0)
    room_auth_level = models.ForeignKey(
        RoomAuthLevel,
        db_column='room_auth_level_id',
        related_name='rooms',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    rental_type = models.ForeignKey(
        RentalType,
        db_column='rental_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    is_sublease = models.BooleanField(_('is_sublease'), db_column='is_sublease', db_index=True, default=False)

    is_condo_management = models.BooleanField(_('is_condo_management'), db_column='is_condo_management', db_index=True, default=False)
    condo_owner = models.ForeignKey(
        Owner,
        db_column='condo_owner_id',
        related_name='condo_rooms',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    is_entrusted = models.BooleanField(_('is_entrusted'), db_column='is_entrusted', db_index=True, default=False)
    condo_trader = models.ForeignKey(
        Trader,
        db_column='condo_trader_id',
        related_name='condo_rooms',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )

    room_status = models.ForeignKey(
        RoomStatus,
        db_column='room_status_id',
        related_name='rooms',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    vacancy_status = models.ForeignKey(
        VacancyStatus,
        db_column='vacancy_status_id',
        related_name='rooms',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    vacancy_status_note = models.TextField(_('vacancy_status_note'), db_column='vacancy_status_note', max_length=2000, null=True, blank=True)

    live_start_year = models.IntegerField(_('live_start_year'), db_column='live_start_year', default=0)
    live_start_month = models.IntegerField(_('live_start_month'), db_column='live_start_month', default=0)
    live_start_day = models.ForeignKey(
        MonthDay,
        db_column='live_start_day_id',
        related_name='live_start_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    live_start_note = models.CharField(_('live_start_note'), db_column='live_start_note', max_length=255, null=True, blank=True)
    cancel_scheduled_year = models.IntegerField(_('cancel_scheduled_year'), db_column='cancel_scheduled_year', default=0)
    cancel_scheduled_month = models.IntegerField(_('cancel_scheduled_month'), db_column='cancel_scheduled_month', default=0)
    cancel_scheduled_day = models.ForeignKey(
        MonthDay,
        db_column='cancel_scheduled_day_id',
        related_name='cancel_scheduled_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    cancel_scheduled_note = models.CharField(_('cancel_scheduled_note'), db_column='cancel_scheduled_note', max_length=255, null=True, blank=True)

    is_publish_vacancy = models.BooleanField(_('is_publish_vacancy'), db_column='is_publish_vacancy', db_index=True, default=True)
    vacancy_start_date = models.CharField(_('vacancy_start_date'), db_column='vacancy_start_date', max_length=10, db_index=True, null=True, blank=True)
    vacancy_end_date = models.CharField(_('vacancy_end_date'), db_column='vacancy_end_date', max_length=10, db_index=True, null=True, blank=True)
    vacancy_catch_copy = models.CharField(_('vacancy_catch_copy'), db_column='vacancy_catch_copy', max_length=100, null=True, blank=True)
    vacancy_appeal = models.CharField(_('vacancy_appeal'), db_column='vacancy_appeal', max_length=255, null=True, blank=True)
    vacancy_note = models.TextField(_('vacancy_note'), db_column='vacancy_note', max_length=2000, null=True, blank=True)
    pending_trader_name = models.CharField(_('pending_trader_name'), db_column='pending_trader_name', max_length=100, null=True, blank=True)
    pending_start_date = models.CharField(_('pending_start_date'), db_column='pending_start_date', max_length=10, null=True, blank=True)
    pending_end_date = models.CharField(_('pending_end_date'), db_column='pending_end_date', max_length=10, null=True, blank=True)
    pending_note = models.CharField(_('pending_note'), db_column='pending_note', max_length=255, null=True, blank=True)

    is_publish_web = models.BooleanField(_('is_publish_web'), db_column='is_publish_web', db_index=True, default=True)
    web_catch_copy = models.CharField(_('web_catch_copy'), db_column='web_catch_copy', max_length=100, null=True, blank=True)
    web_appeal = models.CharField(_('web_appeal'), db_column='web_appeal', max_length=255, null=True, blank=True)
    web_note = models.TextField(_('web_note'), db_column='web_note', max_length=2000, null=True, blank=True)

    layout_type = models.ForeignKey(
        LayoutType,
        db_column='layout_type_id',
        related_name='rooms',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    western_style_room1 = models.DecimalField(_('western_style_room1'), db_column='western_style_room1', default=0, max_digits=5, decimal_places=2)
    western_style_room2 = models.DecimalField(_('western_style_room2'), db_column='western_style_room2', default=0, max_digits=5, decimal_places=2)
    western_style_room3 = models.DecimalField(_('western_style_room3'), db_column='western_style_room3', default=0, max_digits=5, decimal_places=2)
    western_style_room4 = models.DecimalField(_('western_style_room4'), db_column='western_style_room4', default=0, max_digits=5, decimal_places=2)
    western_style_room5 = models.DecimalField(_('western_style_room5'), db_column='western_style_room5', default=0, max_digits=5, decimal_places=2)
    western_style_room6 = models.DecimalField(_('western_style_room6'), db_column='western_style_room6', default=0, max_digits=5, decimal_places=2)
    western_style_room7 = models.DecimalField(_('western_style_room7'), db_column='western_style_room7', default=0, max_digits=5, decimal_places=2)
    western_style_room8 = models.DecimalField(_('western_style_room8'), db_column='western_style_room8', default=0, max_digits=5, decimal_places=2)
    western_style_room9 = models.DecimalField(_('western_style_room9'), db_column='western_style_room9', default=0, max_digits=5, decimal_places=2)
    western_style_room10 = models.DecimalField(_('western_style_room10'), db_column='western_style_room10', default=0, max_digits=5, decimal_places=2)
    japanese_style_room1 = models.DecimalField(_('japanese_style_room1'), db_column='japanese_style_room1', default=0, max_digits=5, decimal_places=2)
    japanese_style_room2 = models.DecimalField(_('japanese_style_room2'), db_column='japanese_style_room2', default=0, max_digits=5, decimal_places=2)
    japanese_style_room3 = models.DecimalField(_('japanese_style_room3'), db_column='japanese_style_room3', default=0, max_digits=5, decimal_places=2)
    japanese_style_room4 = models.DecimalField(_('japanese_style_room4'), db_column='japanese_style_room4', default=0, max_digits=5, decimal_places=2)
    japanese_style_room5 = models.DecimalField(_('japanese_style_room5'), db_column='japanese_style_room5', default=0, max_digits=5, decimal_places=2)
    japanese_style_room6 = models.DecimalField(_('japanese_style_room6'), db_column='japanese_style_room6', default=0, max_digits=5, decimal_places=2)
    japanese_style_room7 = models.DecimalField(_('japanese_style_room7'), db_column='japanese_style_room7', default=0, max_digits=5, decimal_places=2)
    japanese_style_room8 = models.DecimalField(_('japanese_style_room8'), db_column='japanese_style_room8', default=0, max_digits=5, decimal_places=2)
    japanese_style_room9 = models.DecimalField(_('japanese_style_room9'), db_column='japanese_style_room9', default=0, max_digits=5, decimal_places=2)
    japanese_style_room10 = models.DecimalField(_('japanese_style_room10'), db_column='japanese_style_room10', default=0, max_digits=5, decimal_places=2)
    kitchen_type1 = models.ForeignKey(
        KitchenType,
        db_column='kitchen_type_id1',
        related_name='rooms1',
        on_delete=models.PROTECT,
        default=0,
    )
    kitchen1 = models.DecimalField(_('kitchen1'), db_column='kitchen1', default=0, max_digits=5, decimal_places=2)
    kitchen_type2 = models.ForeignKey(
        KitchenType,
        db_column='kitchen_type_id2',
        related_name='rooms2',
        on_delete=models.PROTECT,
        default=0,
    )
    kitchen2 = models.DecimalField(_('kitchen2'), db_column='kitchen2', default=0, max_digits=5, decimal_places=2)
    kitchen_type3 = models.ForeignKey(
        KitchenType,
        db_column='kitchen_type_id3',
        related_name='rooms3',
        on_delete=models.PROTECT,
        default=0,
    )
    kitchen3 = models.DecimalField(_('kitchen3'), db_column='kitchen3', default=0, max_digits=5, decimal_places=2)
    store_room1 = models.DecimalField(_('store_room1'), db_column='store_room1', default=0, max_digits=5, decimal_places=2)
    store_room2 = models.DecimalField(_('store_room2'), db_column='store_room2', default=0, max_digits=5, decimal_places=2)
    store_room3 = models.DecimalField(_('store_room3'), db_column='store_room3', default=0, max_digits=5, decimal_places=2)
    loft1 = models.DecimalField(_('loft1'), db_column='loft1', default=0, max_digits=5, decimal_places=2)
    loft2 = models.DecimalField(_('loft2'), db_column='loft2', default=0, max_digits=5, decimal_places=2)
    sun_room1 = models.DecimalField(_('sun_room1'), db_column='sun_room1', default=0, max_digits=5, decimal_places=2)
    sun_room2 = models.DecimalField(_('sun_room2'), db_column='sun_room2', default=0, max_digits=5, decimal_places=2)
    layout_note = models.CharField(_('layout_note'), db_column='layout_note', max_length=255, null=True, blank=True)
    room_area = models.DecimalField(_('room_area'), db_column='room_area', default=0, max_digits=5, decimal_places=2)

    direction = models.ForeignKey(
        Direction,
        db_column='direction_id',
        related_name='rooms',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    balcony_type = models.ForeignKey(
        BalconyType,
        db_column='balcony_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    balcony_area = models.DecimalField(_('balcony_area'), db_column='balcony_area', default=0, max_digits=5, decimal_places=2)
    rent = models.IntegerField(_('rent'), db_column='rent', db_index=True, default=0)
    rent_upper = models.IntegerField(_('rent_upper'), db_column='rent_upper', db_index=True, default=0)
    trader_rent = models.IntegerField(_('trader_rent'), db_column='trader_rent', db_index=True, default=0)
    rent_tax_type = models.ForeignKey(
        TaxType,
        db_column='rent_tax_type_id',
        related_name='rent_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    rent_hidden = models.BooleanField(_('rent_hidden'), db_column='rent_hidden', default=False)
    condo_fees_type = models.ForeignKey(
        CondoFeesType,
        db_column='condo_fees_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    condo_fees = models.IntegerField(_('condo_fees'), db_column='condo_fees', default=0)
    condo_fees_tax_type = models.ForeignKey(
        TaxType,
        db_column='condo_fees_tax_type_id',
        related_name='condo_fees_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    water_cost_type = models.ForeignKey(
        WaterCostType,
        db_column='water_cost_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    water_cost = models.IntegerField(_('water_cost'), db_column='water_cost', default=0)
    water_cost_tax_type = models.ForeignKey(
        TaxType,
        db_column='water_cost_tax_type_id',
        related_name='water_cost_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    water_check_type = models.ForeignKey(
        WaterCheckType,
        db_column='water_check_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    payment_type = models.ForeignKey(
        PaymentType,
        db_column='payment_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    payment_fee_type = models.ForeignKey(
        PaymentFeeType,
        db_column='payment_fee_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    payment_fee = models.IntegerField(_('payment_fee'), db_column='payment_fee', default=0)
    payment_fee_tax_type = models.ForeignKey(
        TaxType,
        db_column='payment_fee_tax_type_id',
        related_name='payment_fee_rooms',
        on_delete=models.PROTECT,
        default=0,
    )

    monthly_cost_name1 = models.CharField(_('monthly_cost_name1'), db_column='monthly_cost_name1', max_length=100, null=True, blank=True)
    monthly_cost1 = models.IntegerField(_('monthly_cost1'), db_column='monthly_cost1', default=0)
    monthly_cost_tax_type1 = models.ForeignKey(
        TaxType,
        db_column='monthly_cost_tax_type_id1',
        related_name='monthly_cost_rooms1',
        on_delete=models.PROTECT,
        default=0,
    )
    monthly_cost_name2 = models.CharField(_('monthly_cost_name2'), db_column='monthly_cost_name2', max_length=100, null=True, blank=True)
    monthly_cost2 = models.IntegerField(_('monthly_cost2'), db_column='monthly_cost2', default=0)
    monthly_cost_tax_type2 = models.ForeignKey(
        TaxType,
        db_column='monthly_cost_tax_type_id2',
        related_name='monthly_cost_rooms2',
        on_delete=models.PROTECT,
        default=0,
    )
    monthly_cost_name3 = models.CharField(_('monthly_cost_name3'), db_column='monthly_cost_name3', max_length=100, null=True, blank=True)
    monthly_cost3 = models.IntegerField(_('monthly_cost3'), db_column='monthly_cost3', default=0)
    monthly_cost_tax_type3 = models.ForeignKey(
        TaxType,
        db_column='monthly_cost_tax_type_id3',
        related_name='monthly_cost_rooms3',
        on_delete=models.PROTECT,
        default=0,
    )
    monthly_cost_name4 = models.CharField(_('monthly_cost_name4'), db_column='monthly_cost_name4', max_length=100, null=True, blank=True)
    monthly_cost4 = models.IntegerField(_('monthly_cost4'), db_column='monthly_cost4', default=0)
    monthly_cost_tax_type4 = models.ForeignKey(
        TaxType,
        db_column='monthly_cost_tax_type_id4',
        related_name='monthly_cost_rooms4',
        on_delete=models.PROTECT,
        default=0,
    )
    monthly_cost_name5 = models.CharField(_('monthly_cost_name5'), db_column='monthly_cost_name5', max_length=100, null=True, blank=True)
    monthly_cost5 = models.IntegerField(_('monthly_cost5'), db_column='monthly_cost5', default=0)
    monthly_cost_tax_type5 = models.ForeignKey(
        TaxType,
        db_column='monthly_cost_tax_type_id5',
        related_name='monthly_cost_rooms5',
        on_delete=models.PROTECT,
        default=0,
    )
    monthly_cost_name6 = models.CharField(_('monthly_cost_name6'), db_column='monthly_cost_name6', max_length=100, null=True, blank=True)
    monthly_cost6 = models.IntegerField(_('monthly_cost6'), db_column='monthly_cost6', default=0)
    monthly_cost_tax_type6 = models.ForeignKey(
        TaxType,
        db_column='monthly_cost_tax_type_id6',
        related_name='monthly_cost_rooms6',
        on_delete=models.PROTECT,
        default=0,
    )
    monthly_cost_name7 = models.CharField(_('monthly_cost_name7'), db_column='monthly_cost_name7', max_length=100, null=True, blank=True)
    monthly_cost7 = models.IntegerField(_('monthly_cost7'), db_column='monthly_cost7', default=0)
    monthly_cost_tax_type7 = models.ForeignKey(
        TaxType,
        db_column='monthly_cost_tax_type_id7',
        related_name='monthly_cost_rooms7',
        on_delete=models.PROTECT,
        default=0,
    )
    monthly_cost_name8 = models.CharField(_('monthly_cost_name8'), db_column='monthly_cost_name8', max_length=100, null=True, blank=True)
    monthly_cost8 = models.IntegerField(_('monthly_cost8'), db_column='monthly_cost8', default=0)
    monthly_cost_tax_type8 = models.ForeignKey(
        TaxType,
        db_column='monthly_cost_tax_type_id8',
        related_name='monthly_cost_rooms8',
        on_delete=models.PROTECT,
        default=0,
    )
    monthly_cost_name9 = models.CharField(_('monthly_cost_name9'), db_column='monthly_cost_name9', max_length=100, null=True, blank=True)
    monthly_cost9 = models.IntegerField(_('monthly_cost9'), db_column='monthly_cost9', default=0)
    monthly_cost_tax_type9 = models.ForeignKey(
        TaxType,
        db_column='monthly_cost_tax_type_id9',
        related_name='monthly_cost_rooms9',
        on_delete=models.PROTECT,
        default=0,
    )
    monthly_cost_name10 = models.CharField(_('monthly_cost_name10'), db_column='monthly_cost_name10', max_length=100, null=True, blank=True)
    monthly_cost10 = models.IntegerField(_('monthly_cost10'), db_column='monthly_cost10', default=0)
    monthly_cost_tax_type10 = models.ForeignKey(
        TaxType,
        db_column='monthly_cost_tax_type_id10',
        related_name='monthly_cost_rooms10',
        on_delete=models.PROTECT,
        default=0,
    )
    monthly_cost_note = models.TextField(_('monthly_cost_note'), db_column='monthly_cost_note', max_length=2000, null=True, blank=True)
    deposit_type1 = models.ForeignKey(
        DepositType,
        db_column='deposit_type_id1',
        related_name='deposit_type_rooms1',
        on_delete=models.PROTECT,
        default=0,
    )
    deposit_notation1 = models.ForeignKey(
        DepositNotation,
        db_column='deposit_notation_id1',
        related_name='deposit_notation_rooms1',
        on_delete=models.PROTECT,
        default=0,
    )
    deposit_value1 = models.DecimalField(_('deposit_value1'), db_column='deposit_value1', default=0, max_digits=12, decimal_places=2)
    deposit_tax_type1 = models.ForeignKey(
        TaxType,
        db_column='deposit_tax_type_id1',
        related_name='deposit_rooms1',
        on_delete=models.PROTECT,
        default=0,
    )
    deposit_comment1 = models.CharField(_('deposit_comment1'), db_column='deposit_comment1', max_length=100, null=True, blank=True)
    deposit_type2 = models.ForeignKey(
        DepositType,
        db_column='deposit_type_id2',
        related_name='deposit_type_rooms2',
        on_delete=models.PROTECT,
        default=0,
    )
    deposit_notation2 = models.ForeignKey(
        DepositNotation,
        db_column='deposit_notation_id2',
        related_name='deposit_notation_rooms2',
        on_delete=models.PROTECT,
        default=0,
    )
    deposit_value2 = models.DecimalField(_('deposit_value2'), db_column='deposit_value2', default=0, max_digits=12, decimal_places=2)
    deposit_tax_type2 = models.ForeignKey(
        TaxType,
        db_column='deposit_tax_type_id2',
        related_name='deposit_rooms2',
        on_delete=models.PROTECT,
        default=0,
    )
    deposit_comment2 = models.CharField(_('deposit_comment2'), db_column='deposit_comment2', max_length=100, null=True, blank=True)
    key_money_type1 = models.ForeignKey(
        KeyMoneyType,
        db_column='key_money_type_id1',
        related_name='key_money_type_rooms1',
        on_delete=models.PROTECT,
        default=0,
    )
    key_money_notation1 = models.ForeignKey(
        KeyMoneyNotation,
        db_column='key_money_notation_id1',
        related_name='key_money_notation_rooms1',
        on_delete=models.PROTECT,
        default=0,
    )
    key_money_value1 = models.DecimalField(_('key_money_value1'), db_column='key_money_value1', default=0, max_digits=12, decimal_places=2)
    key_money_tax_type1 = models.ForeignKey(
        TaxType,
        db_column='key_money_tax_type_id1',
        related_name='key_money_rooms1',
        on_delete=models.PROTECT,
        default=0,
    )
    key_money_comment1 = models.CharField(_('key_money_comment1'), db_column='key_money_comment1', max_length=100, null=True, blank=True)
    key_money_type2 = models.ForeignKey(
        KeyMoneyType,
        db_column='key_money_type_id2',
        related_name='key_money_type_rooms2',
        on_delete=models.PROTECT,
        default=0,
    )
    key_money_notation2 = models.ForeignKey(
        KeyMoneyNotation,
        db_column='key_money_notation_id2',
        related_name='key_money_notation_rooms2',
        on_delete=models.PROTECT,
        default=0,
    )
    key_money_value2 = models.DecimalField(_('key_money_value2'), db_column='key_money_value2', default=0, max_digits=12, decimal_places=2)
    key_money_tax_type2 = models.ForeignKey(
        TaxType,
        db_column='key_money_tax_type_id2',
        related_name='key_money_rooms2',
        on_delete=models.PROTECT,
        default=0,
    )
    key_money_comment2 = models.CharField(_('key_money_comment2'), db_column='key_money_comment2', max_length=100, null=True, blank=True)
    contract_years = models.IntegerField(_('contract_years'), db_column='contract_years', default=0)
    contract_months = models.IntegerField(_('contract_months'), db_column='contract_months', default=0)
    renewal_fee_notation = models.ForeignKey(
        RenewalFeeNotation,
        db_column='renewal_fee_notation_id',
        related_name='renewal_fee_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    renewal_fee_value = models.DecimalField(_('renewal_fee_value'), db_column='renewal_fee_value', default=0, max_digits=12, decimal_places=2)
    renewal_fee_tax_type = models.ForeignKey(
        TaxType,
        db_column='renewal_fee_tax_type_id',
        related_name='renewal_fee_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    renewal_charge_existence = models.ForeignKey(
        Existence,
        db_column='renewal_charge_existence_id',
        related_name='renewal_charge_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    renewal_charge = models.IntegerField(_('renewal_charge'), db_column='renewal_charge', default=0)
    renewal_charge_tax_type = models.ForeignKey(
        TaxType,
        db_column='renewal_charge_tax_type_id',
        related_name='renewal_charge_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    is_auto_renewal = models.BooleanField(_('is_auto_renewal'), db_column='is_auto_renewal', default=False)
    renewal_note = models.CharField(_('renewal_note'), db_column='renewal_note', max_length=255, null=True, blank=True)
    recontract_fee_existence = models.ForeignKey(
        Existence,
        db_column='recontract_fee_existence_id',
        related_name='recontract_fee_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    recontract_fee = models.IntegerField(_('recontract_fee'), db_column='recontract_fee', default=0)
    recontract_fee_tax_type = models.ForeignKey(
        TaxType,
        db_column='recontract_fee_tax_type_id',
        related_name='recontract_fee_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    recontract_note = models.CharField(_('recontract_note'), db_column='recontract_note', max_length=255, null=True, blank=True)

    insurance_type = models.ForeignKey(
        InsuranceType,
        db_column='insurance_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    insurance_company = models.CharField(_('insurance_company'), db_column='insurance_company', max_length=100, null=True, blank=True)
    insurance_years = models.IntegerField(_('insurance_years'), db_column='insurance_years', default=0)
    insurance_fee = models.IntegerField(_('insurance_fee'), db_column='insurance_fee', default=0)
    insurance_fee_tax_type = models.ForeignKey(
        TaxType,
        db_column='insurance_fee_tax_type_id',
        related_name='insurance_fee_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    guarantee_type = models.ForeignKey(
        GuaranteeType,
        db_column='guarantee_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    guarantee_company = models.CharField(_('guarantee_company'), db_column='guarantee_company', max_length=100, null=True, blank=True)
    guarantee_fee = models.CharField(_('guarantee_fee'), db_column='guarantee_fee', max_length=255, null=True, blank=True)

    document_cost_existence = models.ForeignKey(
        Existence,
        db_column='document_cost_existence_id',
        related_name='document_cost_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    document_cost = models.IntegerField(_('document_cost'), db_column='document_cost', default=0)
    document_cost_tax_type = models.ForeignKey(
        TaxType,
        db_column='document_cost_tax_type_id',
        related_name='document_cost_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    document_cost_comment = models.CharField(_('document_cost_comment'), db_column='document_cost_comment', max_length=100, null=True, blank=True)
    key_change_cost_existence = models.ForeignKey(
        Existence,
        db_column='key_change_cost_existence_id',
        related_name='key_change_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    key_change_cost = models.IntegerField(_('key_change_cost'), db_column='key_change_cost', default=0)
    key_change_cost_tax_type = models.ForeignKey(
        TaxType,
        db_column='key_change_cost_tax_type_id',
        related_name='key_change_cost_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    key_change_comment = models.CharField(_('key_change_comment'), db_column='key_change_comment', max_length=100, null=True, blank=True)

    initial_cost_name1 = models.CharField(_('initial_cost_name1'), db_column='initial_cost_name1', max_length=100, null=True, blank=True)
    initial_cost1 = models.IntegerField(_('initial_cost1'), db_column='initial_cost1', default=0)
    initial_cost_tax_type1 = models.ForeignKey(
        TaxType,
        db_column='initial_cost_tax_type_id1',
        related_name='initial_cost_rooms1',
        on_delete=models.PROTECT,
        default=0,
    )
    initial_cost_name2 = models.CharField(_('initial_cost_name2'), db_column='initial_cost_name2', max_length=100, null=True, blank=True)
    initial_cost2 = models.IntegerField(_('initial_cost2'), db_column='initial_cost2', default=0)
    initial_cost_tax_type2 = models.ForeignKey(
        TaxType,
        db_column='initial_cost_tax_type_id2',
        related_name='initial_cost_rooms2',
        on_delete=models.PROTECT,
        default=0,
    )
    initial_cost_name3 = models.CharField(_('initial_cost_name3'), db_column='initial_cost_name3', max_length=100, null=True, blank=True)
    initial_cost3 = models.IntegerField(_('initial_cost3'), db_column='initial_cost3', default=0)
    initial_cost_tax_type3 = models.ForeignKey(
        TaxType,
        db_column='initial_cost_tax_type_id3',
        related_name='initial_cost_rooms3',
        on_delete=models.PROTECT,
        default=0,
    )
    initial_cost_name4 = models.CharField(_('initial_cost_name4'), db_column='initial_cost_name4', max_length=100, null=True, blank=True)
    initial_cost4 = models.IntegerField(_('initial_cost4'), db_column='initial_cost4', default=0)
    initial_cost_tax_type4 = models.ForeignKey(
        TaxType,
        db_column='initial_cost_tax_type_id4',
        related_name='initial_cost_rooms4',
        on_delete=models.PROTECT,
        default=0,
    )
    initial_cost_name5 = models.CharField(_('initial_cost_name5'), db_column='initial_cost_name5', max_length=100, null=True, blank=True)
    initial_cost5 = models.IntegerField(_('initial_cost5'), db_column='initial_cost5', default=0)
    initial_cost_tax_type5 = models.ForeignKey(
        TaxType,
        db_column='initial_cost_tax_type_id5',
        related_name='initial_cost_rooms5',
        on_delete=models.PROTECT,
        default=0,
    )
    initial_cost_name6 = models.CharField(_('initial_cost_name6'), db_column='initial_cost_name6', max_length=100, null=True, blank=True)
    initial_cost6 = models.IntegerField(_('initial_cost6'), db_column='initial_cost6', default=0)
    initial_cost_tax_type6 = models.ForeignKey(
        TaxType,
        db_column='initial_cost_tax_type_id6',
        related_name='initial_cost_rooms6',
        on_delete=models.PROTECT,
        default=0,
    )
    initial_cost_name7 = models.CharField(_('initial_cost_name7'), db_column='initial_cost_name7', max_length=100, null=True, blank=True)
    initial_cost7 = models.IntegerField(_('initial_cost7'), db_column='initial_cost7', default=0)
    initial_cost_tax_type7 = models.ForeignKey(
        TaxType,
        db_column='initial_cost_tax_type_id7',
        related_name='initial_cost_rooms7',
        on_delete=models.PROTECT,
        default=0,
    )
    initial_cost_name8 = models.CharField(_('initial_cost_name8'), db_column='initial_cost_name8', max_length=100, null=True, blank=True)
    initial_cost8 = models.IntegerField(_('initial_cost8'), db_column='initial_cost8', default=0)
    initial_cost_tax_type8 = models.ForeignKey(
        TaxType,
        db_column='initial_cost_tax_type_id8',
        related_name='initial_cost_rooms8',
        on_delete=models.PROTECT,
        default=0,
    )
    initial_cost_name9 = models.CharField(_('initial_cost_name9'), db_column='initial_cost_name9', max_length=100, null=True, blank=True)
    initial_cost9 = models.IntegerField(_('initial_cost9'), db_column='initial_cost9', default=0)
    initial_cost_tax_type9 = models.ForeignKey(
        TaxType,
        db_column='initial_cost_tax_type_id9',
        related_name='initial_cost_rooms9',
        on_delete=models.PROTECT,
        default=0,
    )
    initial_cost_name10 = models.CharField(_('initial_cost_name10'), db_column='initial_cost_name10', max_length=100, null=True, blank=True)
    initial_cost10 = models.IntegerField(_('initial_cost10'), db_column='initial_cost10', default=0)
    initial_cost_tax_type10 = models.ForeignKey(
        TaxType,
        db_column='initial_cost_tax_type_id10',
        related_name='initial_cost_rooms10',
        on_delete=models.PROTECT,
        default=0,
    )
    initial_cost_note = models.TextField(_('initial_cost_note'), db_column='initial_cost_note', max_length=2000, null=True, blank=True)

    free_rent_type = models.ForeignKey(
        FreeRentType,
        db_column='free_rent_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    free_rent_months = models.IntegerField(_('free_rent_months'), db_column='free_rent_months', default=0)
    free_rent_limit_year = models.IntegerField(_('free_rent_limit_year'), db_column='free_rent_limit_year', default=0)
    free_rent_limit_month = models.IntegerField(_('free_rent_limit_month'), db_column='free_rent_limit_month', default=0)
    cancel_notice_limit = models.IntegerField(_('cancel_notice_limit'), db_column='cancel_notice_limit', default=0)
    cancel_note = models.CharField(_('cancel_note'), db_column='cancel_note', max_length=255, null=True, blank=True)
    short_cancel_note = models.CharField(_('short_cancel_note'), db_column='short_cancel_note', max_length=255, null=True, blank=True)
    cleaning_type = models.ForeignKey(
        CleaningType,
        db_column='cleaning_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    cleaning_cost = models.IntegerField(_('cleaning_cost'), db_column='cleaning_cost', default=0)
    cleaning_cost_tax_type = models.ForeignKey(
        TaxType,
        db_column='cleaning_cost_tax_type_id',
        related_name='cleaning_cost_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    cleaning_note = models.CharField(_('cleaning_note'), db_column='cleaning_note', max_length=255, null=True, blank=True)

    special_agreement = models.TextField(_('special_agreement'), db_column='special_agreement', max_length=2000, null=True, blank=True)

    electric_type = models.ForeignKey(
        ElectricType,
        db_column='electric_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    electric_comment = models.CharField(_('electric_comment'), db_column='electric_comment', max_length=100, null=True, blank=True)
    gas_type = models.ForeignKey(
        GasType,
        db_column='gas_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    gas_comment = models.CharField(_('gas_comment'), db_column='gas_comment', max_length=100, null=True, blank=True)
    bath_type = models.ForeignKey(
        BathType,
        db_column='bath_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    bath_comment = models.CharField(_('bath_comment'), db_column='bath_comment', max_length=100, null=True, blank=True)
    toilet_type = models.ForeignKey(
        ToiletType,
        db_column='toilet_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    toilet_comment = models.CharField(_('toilet_comment'), db_column='toilet_comment', max_length=100, null=True, blank=True)
    kitchen_range_type = models.ForeignKey(
        KitchenRangeType,
        db_column='kitchen_range_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    kitchen_range_comment = models.CharField(_('kitchen_range_comment'), db_column='kitchen_range_comment', max_length=100, null=True, blank=True)
    internet_type = models.ForeignKey(
        InternetType,
        db_column='internet_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    internet_comment = models.CharField(_('internet_comment'), db_column='internet_comment', max_length=100, null=True, blank=True)
    washer_type = models.ForeignKey(
        WasherType,
        db_column='washer_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    washer_comment = models.CharField(_('washer_comment'), db_column='washer_comment', max_length=100, null=True, blank=True)

    pet_type = models.ForeignKey(
        PetType,
        db_column='pet_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    pet_comment = models.CharField(_('pet_comment'), db_column='pet_comment', max_length=100, null=True, blank=True)
    instrument_type = models.ForeignKey(
        AllowType,
        db_column='instrument_type_id',
        related_name='instrument_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    live_together_type = models.ForeignKey(
        AllowType,
        db_column='live_together_type_id',
        related_name='live_together_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    children_type = models.ForeignKey(
        AllowType,
        db_column='children_type_id',
        related_name='children_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    share_type = models.ForeignKey(
        AllowType,
        db_column='share_type_id',
        related_name='share_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    non_japanese_type = models.ForeignKey(
        AllowType,
        db_column='non_japanese_type_id',
        related_name='non_japanese_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    only_woman_type = models.ForeignKey(
        AllowType,
        db_column='only_woman_type_id',
        related_name='only_woman_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    only_man_type = models.ForeignKey(
        AllowType,
        db_column='only_man_type_id',
        related_name='only_man_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    corp_contract_type = models.ForeignKey(
        AllowType,
        db_column='corp_contract_type_id',
        related_name='corp_contract_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    student_type = models.ForeignKey(
        AllowType,
        db_column='student_type_id',
        related_name='student_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    new_student_type = models.ForeignKey(
        AllowType,
        db_column='new_student_type_id',
        related_name='new_student_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    welfare_type = models.ForeignKey(
        AllowType,
        db_column='welfare_type_id',
        related_name='welfare_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    office_use_type = models.ForeignKey(
        AllowType,
        db_column='office_use_type_id',
        related_name='office_use_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    constraint_note = models.CharField(_('constraint_note'), db_column='constraint_note', max_length=255, null=True, blank=True)

    reform_comment = models.CharField(_('reform_comment'), db_column='reform_comment', max_length=100, null=True, blank=True)
    reform_year = models.IntegerField(_('reform_year'), db_column='reform_year', default=0)
    reform_month = models.IntegerField(_('reform_month'), db_column='reform_month', default=0)
    reform_note = models.CharField(_('reform_note'), db_column='reform_note', max_length=255, null=True, blank=True)

    trader_publish_type = models.ForeignKey(
        AllowType,
        db_column='trader_publish_type_id',
        related_name='trader_publish_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    trader_publish_note = models.CharField(_('trader_publish_note'), db_column='trader_publish_note', max_length=255, null=True, blank=True)
    trader_portal_type = models.ForeignKey(
        AllowType,
        db_column='trader_portal_type_id',
        related_name='trader_portal_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    trader_portal_note = models.CharField(_('trader_portal_note'), db_column='trader_portal_note', max_length=255, null=True, blank=True)
    ad_type = models.ForeignKey(
        AdType,
        db_column='ad_type_id',
        related_name='ad_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    ad_value = models.DecimalField(_('ad_value'), db_column='ad_value', default=0, max_digits=12, decimal_places=2)
    ad_tax_type = models.ForeignKey(
        TaxType,
        db_column='ad_tax_type_id',
        related_name='ad_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    trader_ad_type = models.ForeignKey(
        AdType,
        db_column='trader_ad_type_id',
        related_name='trader_ad_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    trader_ad_value = models.DecimalField(_('trader_ad_value'), db_column='trader_ad_value', default=0, max_digits=12, decimal_places=2)
    trader_ad_tax_type = models.ForeignKey(
        TaxType,
        db_column='trader_ad_tax_type_id',
        related_name='trader_ad_rooms',
        on_delete=models.PROTECT,
        default=0,
    )
    owner_fee_type = models.ForeignKey(
        OwnerFeeType,
        db_column='owner_fee_type_id',
        related_name='rooms',
        on_delete=models.PROTECT,
        default=0,
    )

    key_no = models.CharField(_('key_no'), db_column='key_no', max_length=50, null=True, blank=True)
    key_place_note = models.CharField(_('key_place_note'), db_column='key_place_note', max_length=255, null=True, blank=True)
    private_note = models.TextField(_('private_note'), db_column='private_note', max_length=2000, null=True, blank=True)
    management_note = models.TextField(_('management_note'), db_column='management_note', max_length=2000, null=True, blank=True)

    is_deleted = models.BooleanField(_('is_deleted'), db_column='is_deleted', db_index=True, default=False)

    class Meta:
        managed = False
        db_table = 'room'
        ordering = ['building_id', 'room_no', 'id']
        verbose_name = _('room')
        verbose_name_plural = _('rooms')

    def __str__(self):
        return self.room_no

    """
    内部メソッド
    """
    @staticmethod
    def __cost_text(cost_name, cost, tax_type):
        ans = None
        if cost_name and cost > 0:
            ans = '{:,} 円'.format(cost)
            if tax_type.text:
                ans += '({0})'.format(tax_type.text)

        return ans

    @staticmethod
    def __deposit_type_text(deposit_type):
        ans = None
        if deposit_type.id != 0:
            ans = deposit_type.name

        return ans

    @staticmethod
    def __deposit_text(deposit_type, notation, value, tax_type):
        ans = None

        if deposit_type.id != 0:
            if notation.is_money:
                ans = ' {0:,.0f} {1}'.format(value, notation.unit)
                if tax_type.text:
                    ans = '（{0}）'.format(tax_type.text)
            elif notation.is_month:
                ans = ' 賃料 {0} {1}'.format(float_normalize(xfloat(value)), notation.unit)
                if tax_type.text:
                    ans = '（{0}）'.format(tax_type.text)
            elif notation.is_rate:
                ans = ' 賃料の {0:.0f} {1}'.format(value, notation.unit)
                if tax_type.text:
                    ans = '（{0}）'.format(tax_type.text)
            else:
                ans = ' {0}'.format(notation.name)

        return ans

    @staticmethod
    def __key_money_type_text(key_money_type):
        ans = None
        if key_money_type.id != 0:
            ans = key_money_type.name

        return ans

    @staticmethod
    def __key_money_text(key_money_type, notation, value, tax_type):
        ans = None

        if key_money_type.id != 0:
            if notation.is_money:
                ans = ' {0:,.0f} {1}'.format(value, notation.unit)
                if tax_type.text:
                    ans = '（{0}）'.format(tax_type.text)
            elif notation.is_month:
                ans = ' 賃料 {0} {1}'.format(float_normalize(xfloat(value)), notation.unit)
                if tax_type.text:
                    ans = '（{0}）'.format(tax_type.text)
            elif notation.is_rate:
                ans = ' 賃料の {0:.0f} {1}'.format(value, notation.unit)
                if tax_type.text:
                    ans = '（{0}）'.format(tax_type.text)
            else:
                ans = ' {0}'.format(notation.name)

        return ans

    @staticmethod
    def __add_layout_room(type_name, area, target):
        # 洋室・和室・キッチン
        ans = target
        if area > 0:
            if ans:
                ans += '×'
            else:
                ans = ''

            ans += '{0}{1}帖'.format(type_name, float_normalize(xfloat(area)))

        return ans

    @staticmethod
    def __add_layout_space(type_name, area, target):
        # 洋室・和室・キッチン以外
        ans = target
        if area > 0:
            if ans:
                ans += '・'
            else:
                ans = ''

            ans += '{0}{1}帖'.format(type_name, float_normalize(xfloat(area)))

        return ans

    @staticmethod
    def __get_date_string(year: int, month: int, day: MonthDay):
        ans = None
        if year > 0 and 1 <= month <= 12 and day:
            ans = '{0}年{1}月'.format(year, month, day.name)
            if day.id != 0:
                ans += day.name

        return ans

    """
    プロパティ
    """
    @property
    def idb64(self):
        return base64_decode_id(self.pk)

    @property
    def equipments(self):
        return self.room_equipments.filter(
            is_deleted=False,
        ).order_by('priority', 'equipment__category__priority', 'equipment__priority', 'id').all()

    @property
    def movies(self):
        return self.room_movies.filter(
            is_publish_vacancy=True,
            is_deleted=False,
        ).order_by('priority', 'movie_type__priority', 'id').all()

    @property
    def panoramas(self):
        return self.room_panoramas.filter(
            is_publish_vacancy=True,
            is_deleted=False,
        ).order_by('priority', 'panorama_type__priority', 'id').all()

    @property
    def pictures(self):
        return self.room_pictures.filter(
            is_publish_vacancy=True,
            is_deleted=False,
        ).order_by('priority', 'picture_type__priority').all()

    """
    表示用プロパティ
    """
    @property
    def is_no_publish(self):
        ans = False

        if not self.is_publish_vacancy:
            ans = True
        else:
            if self.vacancy_start_date:
                if self.vacancy_start_date >= timezone.now().date().strftime('%Y-%m-%d'):
                    ans = True
            if self.vacancy_end_date:
                if self.vacancy_end_date <= timezone.now().date().strftime('%Y-%m-%d'):
                    ans = True

        return ans

    @property
    def is_high_auth_level(self):
        ans = False

        if self.room_auth_level.level > settings.STANDARD_AUTH_LEVEL:
            ans = True

        return ans

    @property
    def room_floor_text(self):
        ans = None
        if self.room_floor > 0:
            ans = '{0}階'.format(self.room_floor)
        elif self.room_floor < 0:
            ans = '地下{0}階'.format(self.room_floor * -1)
        return ans

    @property
    def rent_text(self):
        ans = None
        if self.rent_hidden:
            ans = "相談"
        elif self.rent > 0:
            ans = '{:,} 円'.format(self.rent)
            if self.rent_tax_type.text:
                ans += '（{0}）'.format(self.rent_tax_type.text)

        return ans

    @property
    def rent_upper_text(self):
        ans = None
        if not self.rent_hidden and self.rent_upper > self.rent:
            ans = '{:,} 円'.format(self.rent_upper)
            if self.rent_tax_type.text:
                ans += '（{0}）'.format(self.rent_tax_type.text)

        return ans

    @property
    def trader_rent_text(self):
        ans = None
        if self.trader_rent > 0:
            ans = '{:,} 円'.format(self.trader_rent)

            if self.rent_tax_type.text:
                ans += '（{0}）'.format(self.rent_tax_type.text)

        return ans

    @property
    def condo_fees_text(self):
        ans = None
        if self.condo_fees_type.id != 0:
            ans = self.condo_fees_type.name
            if self.condo_fees_type.is_money:
                ans = '{:,} 円'.format(self.condo_fees)

                if self.condo_fees_tax_type.text:
                    ans += '（{0}）'.format(self.condo_fees_tax_type.text)

        return ans

    @property
    def water_cost_text(self):
        ans = None
        if self.water_cost_type.id != 0:
            ans = self.water_cost_type.name
            if self.water_cost_type.is_money:
                ans = '{:,} 円'.format(self.water_cost)

                if self.water_cost_tax_type.text:
                    ans += '（{0}）'.format(self.water_cost_tax_type.text)

        return ans

    @property
    def water_check_text(self):
        ans = None
        if self.water_check_type.id != 0:
            ans = self.water_check_type.name

        return ans

    @property
    def payment_type_text(self):
        ans = None
        if self.payment_type.id != 0:
            ans = self.payment_type.name

        return ans

    @property
    def payment_fee_type_text(self):
        ans = None
        if self.payment_fee_type.id != 0:
            ans = self.payment_fee_type.name

        return ans

    @property
    def payment_fee_text(self):
        ans = None
        if self.payment_fee_type.id != 0:
            if self.payment_fee_type.is_money and self.payment_fee > 0:
                ans = ' {:,} 円'.format(self.payment_fee)
                if self.payment_fee_tax_type.text:
                    ans += '（{0}）'.format(self.payment_fee_tax_type.text)

        return ans

    @property
    def free_rent_text(self):
        ans = None

        if self.free_rent_type.limit_is_span:
            if self.free_rent_months > 0:
                ans = '{0}ヶ月'.format(self.free_rent_months)
        elif self.free_rent_type.limit_is_month:
            if self.free_rent_limit_year > 0 and self.free_rent_limit_month > 0:
                ans = '{0}年{1}月まで'.format(self.free_rent_limit_year, self.free_rent_limit_month)

        return ans

    @property
    def monthly_cost_text1(self):
        return self.__cost_text(
            self.monthly_cost_name1,
            self.monthly_cost1,
            self.monthly_cost_tax_type1)

    @property
    def monthly_cost_text2(self):
        return self.__cost_text(
            self.monthly_cost_name2,
            self.monthly_cost2,
            self.monthly_cost_tax_type2)

    @property
    def monthly_cost_text3(self):
        return self.__cost_text(
            self.monthly_cost_name3,
            self.monthly_cost3,
            self.monthly_cost_tax_type3)

    @property
    def monthly_cost_text4(self):
        return self.__cost_text(
            self.monthly_cost_name4,
            self.monthly_cost4,
            self.monthly_cost_tax_type4)

    @property
    def monthly_cost_text5(self):
        return self.__cost_text(
            self.monthly_cost_name5,
            self.monthly_cost5,
            self.monthly_cost_tax_type5)

    @property
    def monthly_cost_text6(self):
        return self.__cost_text(
            self.monthly_cost_name6,
            self.monthly_cost6,
            self.monthly_cost_tax_type6)

    @property
    def monthly_cost_text7(self):
        return self.__cost_text(
            self.monthly_cost_name7,
            self.monthly_cost7,
            self.monthly_cost_tax_type7)

    @property
    def monthly_cost_text8(self):
        return self.__cost_text(
            self.monthly_cost_name8,
            self.monthly_cost8,
            self.monthly_cost_tax_type8)

    @property
    def monthly_cost_text9(self):
        return self.__cost_text(
            self.monthly_cost_name9,
            self.monthly_cost9,
            self.monthly_cost_tax_type9)

    @property
    def monthly_cost_text10(self):
        return self.__cost_text(
            self.monthly_cost_name10,
            self.monthly_cost10,
            self.monthly_cost_tax_type10)

    @property
    def deposit_type_text1(self):
        return self.__deposit_type_text(self.deposit_type1)

    @property
    def deposit_text1(self):
        return self.__deposit_text(
            self.deposit_type1,
            self.deposit_notation1,
            self.deposit_value1,
            self.deposit_tax_type1)

    @property
    def deposit_type_text2(self):
        return self.__deposit_type_text(self.deposit_type2)

    @property
    def deposit_text2(self):
        return self.__deposit_text(
            self.deposit_type2,
            self.deposit_notation2,
            self.deposit_value2,
            self.deposit_tax_type2)

    @property
    def key_money_type_text1(self):
        return self.__key_money_type_text(self.key_money_type1)

    @property
    def key_money_text1(self):
        return self.__key_money_text(
            self.key_money_type1,
            self.key_money_notation1,
            self.key_money_value1,
            self.key_money_tax_type1)

    @property
    def key_money_type_text2(self):
        return self.__key_money_type_text(self.key_money_type2)

    @property
    def key_money_text2(self):
        return self.__key_money_text(
            self.key_money_type2,
            self.key_money_notation2,
            self.key_money_value2,
            self.key_money_tax_type2)

    @property
    def insurance_type_text(self):
        ans = None

        if self.insurance_type.id != 0:
            if self.insurance_type.is_specified:
                ans = '指定'
            else:
                ans = self.insurance_type.name

        return ans

    @property
    def insurance_company_text(self):
        ans = None
        if self.insurance_type.is_specified and self.insurance_company:
            ans = self.insurance_company

        return ans

    @property
    def insurance_text(self):
        ans = ''

        if self.insurance_type.is_specified:
            if self.insurance_years > 0:
                ans += ' {0}年'.format(self.insurance_years)
            if self.insurance_fee > 0:
                ans += ' {0:,} 円'.format(self.insurance_fee)
                if self.insurance_fee_tax_type.text:
                    ans += '（{0}）'.format(self.insurance_fee_tax_type.text)

        if ans == '':
            ans = None

        return ans

    @property
    def guarantee_type_text(self):
        ans = None
        if self.guarantee_type.id != 0:
            ans = self.guarantee_type.name
        return ans

    @property
    def document_cost_text(self):
        ans = None

        if self.document_cost_existence.is_exists:
            ans = ' {0:,} 円'.format(self.document_cost)
            if self.document_cost_tax_type.text:
                ans += '（{0}）'.format(self.document_cost_tax_type.text)

        return ans

    @property
    def key_change_cost_text(self):
        ans = None

        if self.key_change_cost_existence.is_exists:
            ans = ' {0:,} 円'.format(self.key_change_cost)
            if self.key_change_cost_tax_type.text:
                ans += '（{0}）'.format(self.key_change_cost_tax_type.text)

        return ans

    @property
    def initial_cost_text1(self):
        return self.__cost_text(
            self.initial_cost_name1,
            self.initial_cost1,
            self.initial_cost_tax_type1)

    @property
    def initial_cost_text2(self):
        return self.__cost_text(
            self.initial_cost_name2,
            self.initial_cost2,
            self.initial_cost_tax_type2)

    @property
    def initial_cost_text3(self):
        return self.__cost_text(
            self.initial_cost_name3,
            self.initial_cost3,
            self.initial_cost_tax_type3)

    @property
    def initial_cost_text4(self):
        return self.__cost_text(
            self.initial_cost_name4,
            self.initial_cost4,
            self.initial_cost_tax_type4)

    @property
    def initial_cost_text5(self):
        return self.__cost_text(
            self.initial_cost_name5,
            self.initial_cost5,
            self.initial_cost_tax_type5)

    @property
    def initial_cost_text6(self):
        return self.__cost_text(
            self.initial_cost_name6,
            self.initial_cost6,
            self.initial_cost_tax_type6)

    @property
    def initial_cost_text7(self):
        return self.__cost_text(
            self.initial_cost_name7,
            self.initial_cost7,
            self.initial_cost_tax_type7)

    @property
    def initial_cost_text8(self):
        return self.__cost_text(
            self.initial_cost_name8,
            self.initial_cost8,
            self.initial_cost_tax_type8)

    @property
    def initial_cost_text9(self):
        return self.__cost_text(
            self.initial_cost_name9,
            self.initial_cost9,
            self.initial_cost_tax_type9)

    @property
    def initial_cost_text10(self):
        return self.__cost_text(
            self.initial_cost_name10,
            self.initial_cost10,
            self.initial_cost_tax_type10)

    @property
    def rental_type_text(self):
        ans = None
        if self.rental_type.id != 0:
            ans = self.rental_type.short_name

        return ans

    @property
    def contract_span_text(self):
        ans = None

        if self.contract_years > 0 or self.contract_months > 0:
            ans = ''
            if self.contract_years > 0:
                ans += '{0}年'.format(self.contract_years)
            if self.contract_months > 0:
                ans += '{0}ヶ月'.format(self.contract_months)

            if self.is_auto_renewal:
                ans += '（自動更新）'

        return ans

    @property
    def renewal_fee_text(self):
        ans = None

        if self.renewal_fee_notation.is_money:
            ans = '{0:,.0f} {1}'.format(
                self.renewal_fee_value,
                self.renewal_fee_notation.unit,
            )
            if self.renewal_fee_tax_type.text:
                ans += '{0}）'.format(self.renewal_fee_tax_type.text)
        elif self.renewal_fee_notation.is_month:
            ans = '{0}の {1} {2}'.format(
                self.renewal_fee_notation.header,
                float_normalize(xfloat(self.renewal_fee_value)),
                self.renewal_fee_notation.unit,
            )
            if self.renewal_fee_tax_type.text:
                ans += '（{0}）'.format(self.renewal_fee_tax_type.text)
        elif self.renewal_fee_notation.is_rate:
            ans = '{0}の {1:.0f} {2}'.format(
                self.renewal_fee_notation.header,
                float_normalize(xfloat(self.renewal_fee_value)),
                self.renewal_fee_notation.unit,
            )
            if self.renewal_fee_tax_type.text:
                ans += '（{0}）'.format(self.renewal_fee_tax_type.text)
        elif self.renewal_fee_notation.id != 0:
            ans = '{0}'.format(self.renewal_fee_notation.name)

        return ans

    @property
    def renewal_charge_text(self):
        ans = None

        if self.renewal_charge_existence.is_exists:
            ans = ' {0:,} 円'.format(self.renewal_charge)
            if self.renewal_charge_tax_type.text:
                ans += '（{0}）'.format(self.renewal_charge_tax_type.text)

        return ans

    @property
    def recontract_fee_text(self):
        ans = None

        if self.recontract_fee_existence.is_exists:
            ans = ' {0:,} 円'.format(self.recontract_fee)
            if self.recontract_fee_tax_type.text:
                ans += '（{0}）'.format(self.recontract_fee_tax_type.text)

        return ans

    @property
    def cancel_notice_limit_text(self):
        ans = None

        if self.cancel_notice_limit > 0:
            ans = '{0}ヶ月前'.format(self.cancel_notice_limit)

        return ans

    @property
    def cleaning_cost_text(self):
        ans = None
        if self.cleaning_type.is_paid:
            ans = self.cleaning_type.name
            if self.cleaning_type.is_money:
                ans += ' {0:,} 円'.format(self.cleaning_cost)
                if self.cleaning_cost_tax_type.text:
                    ans += '（{0}）'.format(self.cleaning_cost_tax_type.text)

        return ans

    @property
    def room_area_text(self):
        return float_normalize(xfloat(self.room_area))

    @property
    def balcony_type_text(self):
        ans = None
        if 0 < self.balcony_type.id < 90:
            ans = self.balcony_type.name

        return ans

    @property
    def balcony_area_text(self):
        ans = None
        if 0 < self.balcony_type.id < 90:
            ans = float_normalize(xfloat(self.balcony_area))

        return ans

    @property
    def layout_type_text(self):
        ans = None
        if self.layout_type.id != 0:
            ans = self.layout_type.name
        return ans

    @property
    def layout_detail_text(self):
        ans = None

        # 洋室
        if self.western_style_room1 > 0:
            ans = self.__add_layout_room('洋', self.western_style_room1, ans)
        if self.western_style_room2 > 0:
            ans = self.__add_layout_room('洋', self.western_style_room2, ans)
        if self.western_style_room3 > 0:
            ans = self.__add_layout_room('洋', self.western_style_room3, ans)
        if self.western_style_room4 > 0:
            ans = self.__add_layout_room('洋', self.western_style_room4, ans)
        if self.western_style_room5 > 0:
            ans = self.__add_layout_room('洋', self.western_style_room5, ans)
        if self.western_style_room6 > 0:
            ans = self.__add_layout_room('洋', self.western_style_room6, ans)
        if self.western_style_room7 > 0:
            ans = self.__add_layout_room('洋', self.western_style_room7, ans)
        if self.western_style_room8 > 0:
            ans = self.__add_layout_room('洋', self.western_style_room8, ans)
        if self.western_style_room9 > 0:
            ans = self.__add_layout_room('洋', self.western_style_room9, ans)
        if self.western_style_room10 > 0:
            ans = self.__add_layout_room('洋', self.western_style_room10, ans)

        # 和室
        if self.japanese_style_room1 > 0:
            ans = self.__add_layout_room('和', self.japanese_style_room1, ans)
        if self.japanese_style_room2 > 0:
            ans = self.__add_layout_room('和', self.japanese_style_room2, ans)
        if self.japanese_style_room3 > 0:
            ans = self.__add_layout_room('和', self.japanese_style_room3, ans)
        if self.japanese_style_room4 > 0:
            ans = self.__add_layout_room('和', self.japanese_style_room4, ans)
        if self.japanese_style_room5 > 0:
            ans = self.__add_layout_room('和', self.japanese_style_room5, ans)
        if self.japanese_style_room6 > 0:
            ans = self.__add_layout_room('和', self.japanese_style_room6, ans)
        if self.japanese_style_room7 > 0:
            ans = self.__add_layout_room('和', self.japanese_style_room7, ans)
        if self.japanese_style_room8 > 0:
            ans = self.__add_layout_room('和', self.japanese_style_room8, ans)
        if self.japanese_style_room9 > 0:
            ans = self.__add_layout_room('和', self.japanese_style_room9, ans)
        if self.japanese_style_room10 > 0:
            ans = self.__add_layout_room('和', self.japanese_style_room10, ans)

        # キッチン
        if self.kitchen_type1.notation:
            ans = self.__add_layout_room(self.kitchen_type1.notation, self.kitchen1, ans)
        if self.kitchen_type2.notation:
            ans = self.__add_layout_room(self.kitchen_type1.notation, self.kitchen2, ans)
        if self.kitchen_type3.notation:
            ans = self.__add_layout_room(self.kitchen_type1.notation, self.kitchen3, ans)

        # その他スペース
        space = None

        # 納戸
        if self.store_room1 > 0:
            space = self.__add_layout_space('納戸', self.store_room1, space)
        if self.store_room2 > 0:
            space = self.__add_layout_space('納戸', self.store_room2, space)
        if self.store_room3 > 0:
            space = self.__add_layout_space('納戸', self.store_room3, space)

        # ロフト
        if self.loft1 > 0:
            space = self.__add_layout_space('ロフト', self.loft1, space)
        if self.loft2 > 0:
            space = self.__add_layout_space('ロフト', self.loft2, space)

        # サンルーム
        if self.sun_room1 > 0:
            space = self.__add_layout_space('サンルーム', self.sun_room1, space)
        if self.sun_room2 > 0:
            space = self.__add_layout_space('サンルーム', self.sun_room2, space)

        if space:
            ans += ' + {0}'.format(space)

        return ans

    @property
    def direction_text(self):
        ans = None
        if self.direction.id != 0:
            ans = self.direction.name

        return ans

    @property
    def ad_text(self):
        ans = None
        if self.ad_type.id != 0:
            if self.ad_type.is_money:
                ans = ' {0:,.0f} {1}'.format(
                    self.ad_value,
                    self.ad_type.unit,
                )
                if self.ad_tax_type.text:
                    ans += '（{0}）'.format(self.ad_tax_type.text)
            elif self.ad_type.is_month:
                ans = ' 賃料の {0} {1}'.format(
                    float_normalize(xfloat(self.ad_value)),
                    self.ad_type.unit,
                )
                if self.ad_tax_type.text:
                    ans += '（{0}）'.format(self.ad_tax_type.text)
            else:
                ans = ' {0}'.format(self.ad_type.name)

        return ans

    @property
    def trader_ad_text(self):
        ans = None
        if self.trader_ad_type.id != 0:
            if self.trader_ad_type.is_unknown:
                ans = None
            elif self.trader_ad_type.is_money:
                ans = ' {0:,.0f} {1}'.format(
                    self.trader_ad_value,
                    self.trader_ad_type.unit,
                )
                if self.trader_ad_tax_type.text:
                    ans += '（{0}）'.format(self.trader_ad_tax_type.text)
            elif self.trader_ad_type.is_month:
                ans = ' 賃料の {0} {1}'.format(
                    float_normalize(xfloat(self.trader_ad_value)),
                    self.trader_ad_type.unit,
                )
                if self.trader_ad_tax_type.text:
                    ans += '（{0}）'.format(self.trader_ad_tax_type.text)
            else:
                ans = ' {0}'.format(self.trader_ad_type.name)

        return ans

    @property
    def owner_fee_text(self):
        ans = None
        if self.owner_fee_type.id != 0:
            ans = self.owner_fee_type.name

        return ans

    @property
    def vacancy_status_text(self):
        ans = None
        if self.room_status.for_rent:
            if not self.vacancy_status.id in [0, 90]:
                ans = self.vacancy_status.name

        return ans

    @property
    def live_start_date_text(self):
        ans = None
        if self.room_status.will_be_canceled:
            ans = Room.__get_date_string(
                self.live_start_year,
                self.live_start_month,
                self.live_start_day
            )

        return ans

    @property
    def cancel_scheduled_date_text(self):
        ans = None
        if self.room_status.will_be_canceled:
            ans = Room.__get_date_string(
                self.cancel_scheduled_year,
                self.cancel_scheduled_month,
                self.cancel_scheduled_day
            )

        return ans

    @property
    def electric_text(self):
        ans = None
        if self.electric_type.id != 0:
            ans = self.electric_type.name
        return ans

    @property
    def gas_text(self):
        ans = None
        if self.gas_type.id != 0:
            ans = self.gas_type.name
        return ans

    @property
    def bath_text(self):
        ans = None
        if self.bath_type.id != 0:
            ans = self.bath_type.name
        return ans

    @property
    def toilet_text(self):
        ans = None
        if self.toilet_type.id != 0:
            ans = self.toilet_type.name
        return ans

    @property
    def kitchen_range_text(self):
        ans = None
        if self.kitchen_range_type.id != 0:
            ans = self.kitchen_range_type.name
        return ans

    @property
    def internet_text(self):
        ans = None
        if self.internet_type.id != 0:
            ans = self.internet_type.name
        return ans

    @property
    def washer_text(self):
        ans = None
        if self.washer_type.id != 0:
            ans = self.washer_type.name
        return ans

    @property
    def pet_text(self):
        ans = None
        if self.pet_type.id != 0:
            ans = self.pet_type.name
        return ans

    @property
    def reform_year_month(self):
        ans = None
        if self.reform_year > 0:
            ans = '{0}年'.format(self.reform_year)
            if 1 <= self.reform_month <= 12:
                ans += '{0}月'.format(self.reform_month)

        return ans

    @property
    def trader_publish_text(self):
        ans = None
        if self.trader_publish_type.id != 0:
            ans = self.trader_publish_type.name

        return ans

    @property
    def trader_portal_text(self):
        ans = None
        if self.trader_portal_type.id != 0:
            ans = self.trader_portal_type.name

        return ans

    @property
    def vacancy_theme_appeal_text(self):
        ans = None
        if self.vacancy_appeal:
            ans = self.vacancy_appeal
        elif self.building.vacancy_appeal:
            ans = self.building.vacancy_appeal;

        return ans

    @property
    def vacancy_theme_catch_copy_text(self):
        ans = None
        if self.vacancy_catch_copy:
            ans = self.vacancy_catch_copy
        elif self.building.vacancy_catch_copy:
            ans = self.building.vacancy_catch_copy;

        return ans

    """
    空室条件取得用メソッド
    """
    @staticmethod
    def get_vacancy_room_condition(auth_user: VacancyUser, is_residential: bool, is_non_residential: bool):
        ans = None
        if auth_user:
            if auth_user.is_company:
                # 自社ユーザの場合
                ans = Q(
                    Q(building__management_type__is_own=True) | Q(building__management_type__is_entrusted=True)     # 自社物件、専任物件
                ) | Q(
                    Q(building__management_type__is_condo_management=True),  # 分譲マンション
                    Q(is_sublease=True) | Q(is_condo_management=True) | Q(is_entrusted=True),  # サブリース、分譲管理、分譲専任の部屋
                )

            else:
                # 自社ユーザでない場合
                today = timezone.now().date().strftime('%Y-%m-%d')
                ans = Q(
                    building__management_type__is_own=True,    # 自社物件
                ) | Q(
                    Q(building__management_type__is_condo_management=True),    # 分譲マンション
                    Q(is_sublease=True) | Q(is_condo_management=True),    # サブリース、分譲管理の部屋
                )
                ans.add(Q(
                    Q(is_publish_vacancy=True),     # 空室情報公開の部屋
                    Q(vacancy_start_date=None) | Q(vacancy_start_date__lte=today),
                    Q(vacancy_end_date=None) | Q(vacancy_end_date__gte=today),
                ), Q.AND)     # 空室情報公開中の部屋
                ans.add(Q(room_auth_level__level__lte=auth_user.level.level), Q.AND)        # ユーザ権限レベル
                ans.add(Q(building__is_hidden_vacancy=False), Q.AND)    # 建物が表示対象

            # 居住用と非居住用の指定（両方がFalseの場合は全て）
            if is_residential and is_non_residential:
                ans.add(Q(rental_type__is_residential=True) | Q(rental_type__is_non_residential=True), Q.AND)
            elif is_residential:
                ans.add(Q(rental_type__is_residential=True), Q.AND)
            elif is_non_residential:
                ans.add(Q(rental_type__is_non_residential=True), Q.AND)

            ans.add(Q(room_status__for_rent=True) | Q(room_status__is_pending=True), Q.AND)    # 空き・空き予定・保留
            ans.add(Q(is_deleted=False, building__is_deleted=False), Q.AND)     # 削除されていない

        return ans
