"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from lib.convert import *
from lib.functions import *
from lib.cache_file_helper import CacheFileHelper
from .company import Company
from .picture_type import PictureType


class BuildingPicture(models.Model):
    """
    建物画像
    """
    id = models.AutoField(_('id'), db_column='id', primary_key=True)

    building = models.ForeignKey(
        'Building',
        db_column='building_id',
        related_name='building_pictures',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )

    file_name = models.CharField(_('file_name'), db_column='file_name', max_length=255)
    cache_name_thumb = models.CharField(_('cache_name_thumb'), db_column='cache_name_thumb', max_length=255)
    cache_name_s = models.CharField(_('cache_name_s'), db_column='cache_name_s', max_length=255)
    cache_name_m = models.CharField(_('cache_name_m'), db_column='cache_name_m', max_length=255)
    cache_name_l = models.CharField(_('cache_name_l'), db_column='cache_name_l', max_length=255)
    cache_name_org = models.CharField(_('cache_name_org'), db_column='cache_name_org', max_length=255)
    picture_type = models.ForeignKey(
        PictureType,
        db_column='picture_type_id',
        related_name='building_pictures',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    is_publish_web = models.BooleanField(_('is_publish_web'), db_column='is_publish_web', db_index=True, default=True)
    is_publish_vacancy = models.BooleanField(_('is_publish_vacancy'), db_column='is_publish_vacancy', db_index=True, default=True)
    comment = models.CharField(_('comment'), db_column='comment', max_length=50, null=True, blank=True)
    note = models.CharField(_('note'), db_column='note', max_length=255, null=True, blank=True)
    priority = models.IntegerField(_('priority'), db_column='priority', db_index=True, default=100)

    is_deleted = models.BooleanField(_('is_deleted'), db_column='is_deleted', db_index=True, default=False)

    class Meta:
        managed = False
        db_table = 'building_picture'
        ordering = ['priority', 'id']
        verbose_name = _('building_picture')
        verbose_name_plural = _('building_pictures')

    @property
    def idb64(self):
        return base64_decode_id(self.pk)

    @property
    def thumbnail_file_url(self):
        """サムネイルファイルのURLの取得"""
        return CacheFileHelper.get_property_image_file_url(
            self.building.file_oid,
            self.file_name,
            self.cache_name_thumb,
            Company.get_instance().water_mark,
            settings.THUMBNAIL_IMAGE_SIZE
        )

    @property
    def cache_file_url(self):
        """キャッシュファイルのURLの取得"""
        url = None

        auth_user = self.building.auth_user
        if auth_user:
            cache_file_name = None
            cache_file_size = None
            water_mark = Company.get_instance().water_mark
            if auth_user.is_company or auth_user.allow_org_image:
                cache_file_name = self.cache_name_org
                cache_file_size = settings.ORIGINAL_IMAGE_SIZE
                water_mark = None
            elif auth_user.level.level >= settings.LARGE_IMAGE_LEVEL:
                cache_file_name = self.cache_name_l
                cache_file_size = settings.LARGE_IMAGE_SIZE
            elif auth_user.level.level >= settings.MEDIUM_IMAGE_LEVEL:
                cache_file_name = self.cache_name_m
                cache_file_size = settings.MEDIUM_IMAGE_SIZE
            elif auth_user.level.level >= settings.SMALL_IMAGE_LEVEL:
                cache_file_name = self.cache_name_s
                cache_file_size = settings.SMALL_IMAGE_SIZE

            if cache_file_name and cache_file_size:
                url = CacheFileHelper.get_property_image_file_url(
                    self.building.file_oid,
                    self.file_name,
                    cache_file_name,
                    water_mark,
                    cache_file_size
                )

        return url
