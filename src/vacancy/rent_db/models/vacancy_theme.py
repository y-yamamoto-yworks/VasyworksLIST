"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from django.db import models
from django.db.models import Q, Subquery, OuterRef
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from lib.convert import *
from lib.functions import *
from .area import Area
from .city import City
from .pref import Pref
from .room_auth_level import RoomAuthLevel
from .room import Room
from users.models import VacancyUser


class VacancyTheme(models.Model):
    """
    空室情報テーマ
    """
    id = models.AutoField(_('id'), db_column='id', primary_key=True)

    name = models.CharField(_('name'), db_column='name', max_length=50)
    title = models.CharField(_('title'), db_column='title', max_length=100, null=True, blank=True)
    description = models.CharField(_('description'), db_column='description', max_length=255, null=True, blank=True)
    priority = models.IntegerField(_('priority'), db_column='priority', db_index=True, default=100)
    room_auth_level = models.ForeignKey(
        RoomAuthLevel,
        db_column='room_auth_level_id',
        related_name='vacancy_themes',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    is_publish = models.BooleanField(_('is_publish'), db_column='is_publish', default=False)

    is_stopped = models.BooleanField(_('is_stopped'), db_column='is_stopped', db_index=True, default=False)

    class Meta:
        managed = False
        db_table = 'vacancy_theme'
        ordering = ['priority', 'id']
        verbose_name = _('vacancy_theme')
        verbose_name_plural = _('vacancy_themes')

    def __str__(self):
        return self.name

    @property
    def idb64(self):
        return base64_decode_id(self.pk)

    def get_theme_rooms(self, auth_user: VacancyUser, pref: Pref, city: City, area: Area):
        """テーマ別部屋一覧"""
        if not auth_user:
            raise Exception

        conditions = Q(room_vacancy_themes__vacancy_theme=self)

        if area:
            conditions.add(Q(building__area=area), Q.AND)
        elif city:
            conditions.add(Q(building__city=city), Q.AND)
        elif pref:
            conditions.add(Q(building__pref=pref), Q.AND)

        conditions.add(Room.get_vacancy_room_condition(auth_user, True, False), Q.AND)      # 居住用のみを対象

        rooms = Room.objects.filter(conditions).order_by(
            'building__pref__priority',
            'building__city__priority',
            'building__building_kana',
            'building__id',
            'room_no',
            'id',
        )

        return rooms

    @classmethod
    def get_themes(cls, auth_user: VacancyUser):
        """テーマ一覧"""
        if not auth_user:
            raise Exception

        conditions = Q(is_publish=True, is_stopped=False)

        if not auth_user.is_company:
            conditions.add(Q(room_auth_level__level__lte=auth_user.level.level), Q.AND)

        conditions.add(Q(id=Subquery(
            Room.objects.filter(
                Room.get_vacancy_room_condition(auth_user, True, False)
            ).filter(
                room_vacancy_themes__vacancy_theme_id=OuterRef('pk'),
            ).values('room_vacancy_themes__vacancy_theme_id')[:1])), Q.AND)

        themes = cls.objects.filter(conditions).order_by('priority', 'id')

        return themes
