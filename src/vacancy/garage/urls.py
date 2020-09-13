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
    path('garage_list/', GarageListView.as_view(), name='garage_garage_list'),
    path('garage_list/<int:page_number>', GarageListView.as_view(), name='garage_garage_list'),

    path('', TemplateView.as_view(template_name='404.html'), name='garage_index'),
]
