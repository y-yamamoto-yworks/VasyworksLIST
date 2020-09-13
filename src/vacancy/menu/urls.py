"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from django.urls import include, path
from django.views.generic import TemplateView
from .views import MenuIndexView, VacancyListView

urlpatterns = [
    path('vacancy_list', VacancyListView.as_view(), name="menu_vacancy_list"),

    path('', MenuIndexView.as_view(), name="menu_index"),
]
