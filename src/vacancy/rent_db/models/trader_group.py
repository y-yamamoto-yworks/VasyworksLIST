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


class TraderGroup(models.Model):
    """
    賃貸管理業者グループ
    """
    id = models.AutoField(_('id'), db_column='id', primary_key=True)

    trader_group_name = models.CharField(_('trader_group_name'), db_column='trader_group_name', max_length=255, db_index=True)
    trader_group_kana = models.CharField(_('trader_group_kana'), db_column='trader_group_kana', max_length=255, db_index=True, null=True, blank=True)
    note = models.TextField(_('note'), db_column='note', max_length=2000, null=True, blank=True)

    is_stopped = models.BooleanField(_('is_stopped'), db_column='is_stopped', db_index=True, default=False)
    is_deleted = models.BooleanField(_('is_deleted'), db_column='is_deleted', db_index=True, default=False)

    class Meta:
        managed = False
        db_table = 'trader_group'
        ordering = ['trader_group_kana', 'id']
        verbose_name = _('trader_group')
        verbose_name_plural = _('trader_groups')

    def __str__(self):
        return self.trader_group_name

    @property
    def idb64(self):
        return base64_decode_id(self.pk)
