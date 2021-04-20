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
    path('cache_media/<path:file_url>', CacheMediaViewerView.as_view(), name='viewer_cache_media'),

    path('', TemplateView.as_view(template_name='404.html'), name='viewer_index'),
]
