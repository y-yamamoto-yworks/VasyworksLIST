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
    path('building/<str:idb64>', BuildingPanoramaView.as_view(), name='panorama_building_panorama'),
    path('room/<str:idb64>', RoomPanoramaView.as_view(), name='panorama_room_panorama'),

    path('', TemplateView.as_view(template_name='404.html'), name='panorama_index'),
]
