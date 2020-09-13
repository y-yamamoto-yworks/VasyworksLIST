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
    path('<str:oid>', RoomView.as_view(), name='room_room'),

    path('list/vacancy_theme/<str:idb64>', VacancyThemeRoomListView.as_view(), name='room_vacancy_theme_room_list'),
    path('list/vacancy_theme/<str:idb64>/<int:page_number>', VacancyThemeRoomListView.as_view(), name='room_vacancy_theme_room_list'),

    path('', TemplateView.as_view(template_name='404.html'), name='room_index'),
]
