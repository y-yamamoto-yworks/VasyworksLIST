"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from .models import VacancyUser


class UserBackEnd(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password)

        # 拡張条件がある場合はここで処理

        return user
