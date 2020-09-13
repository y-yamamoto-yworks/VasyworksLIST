"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from django.urls import include, path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('<str:oid>', BuildingView.as_view(), name='building_building'),
    path('garages/<str:oid>', BuildingGarageListView.as_view(), name='building_garage_list'),

    path('list/area/<str:idb64>', AreaResidentialBuildingListView.as_view(), name='building_area_building_list'),
    path('list/area/<str:idb64>/<int:page_number>', AreaResidentialBuildingListView.as_view(), name='building_area_building_list'),
    path('list/city/<str:idb64>', CityResidentialBuildingListView.as_view(), name='building_city_building_list'),
    path('list/city/<str:idb64>/<int:page_number>', CityResidentialBuildingListView.as_view(), name='building_city_building_list'),

    path('list/non_residential/', NonResidentialBuildingListView.as_view(), name='building_non_residential_building_list'),
    path('list/non_residential/<int:page_number>', NonResidentialBuildingListView.as_view(), name='building_non_residential_building_list'),

    path('list/search_name/', SearchNameBuildingListView.as_view(), name='building_search_name_building_list'),
    path('list/search_name/<int:page_number>', SearchNameBuildingListView.as_view(), name='building_search_name_building_list'),

    path('', TemplateView.as_view(template_name='404.html'), name='building_index'),
]
