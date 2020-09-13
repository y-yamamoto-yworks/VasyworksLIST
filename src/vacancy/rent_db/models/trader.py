"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from lib.convert import *
from lib.functions import *
from .trader_group import TraderGroup


class Trader(models.Model):
    """
    賃貸管理業者
    """
    id = models.AutoField(_('id'), db_column='id', primary_key=True)

    trader_group = models.ForeignKey(
        TraderGroup,
        db_column='trader_group_id',
        related_name='traders',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    trader_name = models.CharField(_('trader_name'), db_column='trader_name', max_length=255, db_index=True)
    trader_kana = models.CharField(_('trader_kana'), db_column='trader_kana', max_length=255, db_index=True, null=True, blank=True)
    postal_code = models.CharField(_('postal_code'), db_column='postal_code', max_length=10, null=True, blank=True)
    address = models.CharField(_('address'), db_column='address', max_length=255, null=True, blank=True)
    tel1 = models.CharField(_('tel1'), db_column='tel1', max_length=20, null=True, blank=True)
    tel2 = models.CharField(_('tel2'), db_column='tel2', max_length=20, null=True, blank=True)
    fax = models.CharField(_('fax'), db_column='fax', max_length=20, null=True, blank=True)
    mail = models.EmailField(_('mail'), db_column='mail', null=True, blank=True)
    no_trading = models.BooleanField(_('no_trading'), db_column='no_trading', default=False)
    no_portal = models.BooleanField(_('no_portal'), db_column='no_portal', default=False)
    note = models.TextField(_('note'), db_column='note', max_length=2000, null=True, blank=True)

    is_stopped = models.BooleanField(_('is_stopped'), db_column='is_stopped', db_index=True, default=False)
    is_deleted = models.BooleanField(_('is_deleted'), db_column='is_deleted', db_index=True, default=False)

    class Meta:
        managed = False
        db_table = 'trader'
        ordering = ['trader_kana', 'id']
        verbose_name = _('trader')
        verbose_name_plural = _('traders')

    def __str__(self):
        return self.trader_name

    @property
    def idb64(self):
        return base64_decode_id(self.pk)
