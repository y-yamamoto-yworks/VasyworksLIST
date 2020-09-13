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
from .room_status import RoomStatus


class RoomStatusLog(models.Model):
    """
    部屋状況変更ログ
    """
    id = models.AutoField(_('id'), db_column='id', primary_key=True)

    building = models.ForeignKey(
        'Building',
        db_column='building_id',
        related_name='room_status_logs',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    room = models.ForeignKey(
        'Room',
        db_column='room_id',
        related_name='room_status_logs',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )

    room_status = models.ForeignKey(
        RoomStatus,
        db_column='room_status_id',
        related_name='room_status_logs',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    last_room_status = models.ForeignKey(
        RoomStatus,
        db_column='last_room_status_id',
        related_name='last_room_status_logs',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )

    created_at = models.DateTimeField(_('created_at'), db_column='created_at', default=timezone.now)

    class Meta:
        managed = False
        db_table = 'room_status_log'
        ordering = ['id']
        verbose_name = _('room_status_log')
        verbose_name_plural = _('room_status_logs')

    @property
    def idb64(self):
        return base64_decode_id(self.pk)
