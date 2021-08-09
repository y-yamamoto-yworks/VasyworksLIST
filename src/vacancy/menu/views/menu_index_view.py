"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
import os
import datetime
from abc import ABCMeta, abstractmethod
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, FormView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from dateutil.relativedelta import relativedelta
from PIL import Image
from lib.convert import *
from rent_db.models import *


class MenuIndexView(TemplateView):
    """
    TOPメニュー
    """
    template_name = 'menu/index.html'

    def __init__(self, **kwargs):
        self.user = None

        super().__init__(**kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        if not self.user:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['company'] = Company.get_instance()
        context['display_info_date'] = settings.DISPLAY_INFO_DATE

        context['departments'] = Department.objects.filter(
            is_publish_vacancy=True,
            is_stopped=False,
            is_deleted=False,
        ).order_by('priority', 'id').all()

        context['staffs'] = Staff.objects.filter(
            is_publish_vacancy=True,
            is_stopped=False,
            is_deleted=False,
        ).order_by('department__priority', 'department__id', 'priority', 'id').all()

        context['management_infos'] = ManagementInfo.objects.filter(
            start_date__lte=datetime.date.today().strftime('%Y-%m-%d'),
            end_date__gte=datetime.date.today().strftime('%Y-%m-%d'),
            is_deleted=False,
        ).order_by('priority', '-start_date', '-end_date', '-id').all()

        context['recommended_buildings'] = Building.get_recommended_buildings(self.user)

        return context
