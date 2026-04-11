"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
"""
import urllib.parse
import django_filters
from django.shortcuts import render
from rest_framework import viewsets, filters
from django.db.models import Q
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str, escape_uri_path
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from lib.convert import *
from api.api_helper import ApiHelper
from rent_db.models import City
from api.serializers import CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    """
    市区町村
    """
    @method_decorator(login_required)
    def list(self, request, *args, **kwargs):
        key = kwargs.get('key')
        if not ApiHelper.check_key(key):
            raise Exception

        pref_id = kwargs.get('pref_id')

        self.queryset = City.objects.filter(
            Q(pref_id=pref_id, is_trading_area=True) | Q(pk=0)
        ).order_by('priority').all()
        self.serializer_class = CitySerializer

        return super().list(request, args, kwargs)
