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
    path('building/<str:idb64>', BuildingMovieView.as_view(), name='movie_building_movie'),
    path('room/<str:idb64>', RoomMovieView.as_view(), name='movie_room_movie'),

    path('', TemplateView.as_view(template_name='404.html'), name='movie_index'),
]
