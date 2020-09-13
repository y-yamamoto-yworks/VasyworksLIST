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


class RoomVacancyTheme(models.Model):
    """
    部屋空室情報テーマ
    """
    id = models.AutoField(_('id'), db_column='id', primary_key=True)

    building = models.ForeignKey(
        'Building',
        db_column='building_id',
        related_name='room_vacancy_themes',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    room = models.ForeignKey(
        'Room',
        db_column='room_id',
        related_name='room_vacancy_themes',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )

    vacancy_theme = models.ForeignKey(
        'VacancyTheme',
        db_column='vacancy_theme_id',
        related_name='room_vacancy_themes',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )

    is_deleted = models.BooleanField(_('is_deleted'), db_column='is_deleted', db_index=True, default=False)

    class Meta:
        managed = False
        db_table = 'room_vacancy_theme'
        ordering = ['id']
        verbose_name = _('room_vacancy_theme')
        verbose_name_plural = _('room_vacancy_themes')

    @property
    def idb64(self):
        return base64_decode_id(self.pk)
