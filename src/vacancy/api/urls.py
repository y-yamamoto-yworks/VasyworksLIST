"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
"""
from django.urls import include, path
from django.views.generic import TemplateView
from api.viewsets import *

urlpatterns = [
    path('areas/<int:city_id>', AreaViewSet.as_view({'get': 'list'}), name='api_areas'),
    path('cities/<int:pref_id>', CityViewSet.as_view({'get': 'list'}), name='api_cities'),
    path('prefs/', PrefViewSet.as_view({'get': 'list'}), name='api_prefs'),
]