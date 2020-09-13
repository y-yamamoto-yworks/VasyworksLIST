"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from lib.convert import *
from lib.functions import *
from .garage_status import GarageStatus
from .tax_type import TaxType


class BuildingGarage(models.Model):
    """
    建物駐車場
    """
    id = models.AutoField(_('id'), db_column='id', primary_key=True)

    building = models.ForeignKey(
        'Building',
        db_column='building_id',
        related_name='building_garages',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )

    garage_name = models.CharField(_('garage_name'), db_column='garage_name', max_length=100)
    garage_fee = models.IntegerField(_('garage_fee'), db_column='garage_fee', default=0)
    garage_fee_tax_type = models.ForeignKey(
        TaxType,
        db_column='garage_fee_tax_type_id',
        related_name='garage_fees',
        on_delete=models.PROTECT,
        default=0,
    )
    garage_charge = models.IntegerField(_('garage_charge'), db_column='garage_charge', default=0)
    garage_charge_tax_type = models.ForeignKey(
        TaxType,
        db_column='garage_charge_tax_type_id',
        related_name='garage_charges',
        on_delete=models.PROTECT,
        default=0,
    )
    garage_deposit = models.IntegerField(_('garage_deposit'), db_column='garage_deposit', default=0)
    garage_deposit_tax_type = models.ForeignKey(
        TaxType,
        db_column='garage_deposit_tax_type_id',
        related_name='garage_deposits',
        on_delete=models.PROTECT,
        default=0,
    )
    certification_fee = models.IntegerField(_('certification_fee'), db_column='certification_fee', default=0)
    certification_fee_tax_type = models.ForeignKey(
        TaxType,
        db_column='certification_fee_tax_type_id',
        related_name='certification_fees',
        on_delete=models.PROTECT,
        default=0,
    )
    initial_cost_name1 = models.CharField(_('initial_cost_name1'), db_column='initial_cost_name1', max_length=100, null=True, blank=True)
    initial_cost1 = models.IntegerField(_('initial_cost1'), db_column='initial_cost1', default=0)
    initial_cost_tax_type1 = models.ForeignKey(
        TaxType,
        db_column='initial_cost_tax_type_id1',
        related_name='initial_costs1',
        on_delete=models.PROTECT,
        default=0,
    )
    initial_cost_name2 = models.CharField(_('initial_cost_name2'), db_column='initial_cost_name2', max_length=100, null=True, blank=True)
    initial_cost2 = models.IntegerField(_('initial_cost2'), db_column='initial_cost2', default=0)
    initial_cost_tax_type2 = models.ForeignKey(
        TaxType,
        db_column='initial_cost_tax_type_id2',
        related_name='initial_costs2',
        on_delete=models.PROTECT,
        default=0,
    )
    initial_cost_name3 = models.CharField(_('initial_cost_name3'), db_column='initial_cost_name3', max_length=100, null=True, blank=True)
    initial_cost3 = models.IntegerField(_('initial_cost3'), db_column='initial_cost3', default=0)
    initial_cost_tax_type3 = models.ForeignKey(
        TaxType,
        db_column='initial_cost_tax_type_id3',
        related_name='initial_costs3',
        on_delete=models.PROTECT,
        default=0,
    )
    garage_status = models.ForeignKey(
        GarageStatus,
        db_column='garage_status_id',
        related_name='building_garages',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    allow_no_room = models.BooleanField(_('allow_no_room'), db_column='allow_no_room', db_index=True, default=False)
    width = models.DecimalField(_('width'), db_column='width', default=0, max_digits=12, decimal_places=2)
    length = models.DecimalField(_('length'), db_column='length', default=0, max_digits=12, decimal_places=2)
    height = models.DecimalField(_('height'), db_column='height', default=0, max_digits=12, decimal_places=2)
    comment = models.CharField(_('comment'), db_column='comment', max_length=100, null=True, blank=True)
    note = models.CharField(_('note'), db_column='note', max_length=255, null=True, blank=True)
    priority = models.IntegerField(_('priority'), db_column='priority', db_index=True, default=100)

    is_deleted = models.BooleanField(_('is_deleted'), db_column='is_deleted', db_index=True, default=False)

    class Meta:
        managed = False
        db_table = 'building_garage'
        ordering = ['priority', 'id']
        verbose_name = _('building_garage')
        verbose_name_plural = _('building_garages')

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

    """
    プロパティ
    """
    @property
    def idb64(self):
        return base64_decode_id(self.pk)

    @property
    def garage_status_text(self):
        ans = None
        if self.garage_status.id != 0:
            ans = self.garage_status.name

        return ans

    @property
    def garage_fee_text(self):
        ans = None
        if self.garage_fee > 0:
            ans = '{:,} 円'.format(self.garage_fee)

        if self.garage_fee_tax_type.text:
            ans += '（{0}）'.format(self.garage_fee_tax_type.text)

        return ans

    @property
    def garage_charge_text(self):
        ans = None
        if self.garage_charge > 0:
            ans = '{:,} 円'.format(self.garage_charge)

        if self.garage_charge_tax_type.text:
            ans += '（{0}）'.format(self.garage_charge_tax_type.text)

        return ans

    @property
    def garage_deposit_text(self):
        ans = None
        if self.garage_deposit > 0:
            ans = '{:,} 円'.format(self.garage_deposit)

        if self.garage_deposit_tax_type.text:
            ans += '（{0}）'.format(self.garage_deposit_tax_type.text)

        return ans

    @property
    def certification_fee_text(self):
        ans = None
        if self.certification_fee > 0:
            ans = '{:,} 円'.format(self.certification_fee)

        if self.certification_fee_tax_type.text:
            ans += '（{0}）'.format(self.certification_fee_tax_type.text)

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
    def allow_no_room_text(self):
        ans = None
        if self.allow_no_room:
            ans = '外部貸し可'

        return ans

    @property
    def garage_size_text(self):
        ans = ''
        if self.width > 0:
            ans = '幅{0}m'.format(float_normalize(xfloat(self.width)))
        if self.length > 0:
            if ans != '':
                ans += '×'
            ans += '奥行{0}m'.format(float_normalize(xfloat(self.length)))
        if self.height > 0:
            if ans != '':
                ans += '×'
            ans += '高さ{0}m'.format(float_normalize(xfloat(self.height)))
        if ans == '':
            ans = None

        return ans
