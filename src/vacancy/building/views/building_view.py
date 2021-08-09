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


class BuildingView(TemplateView):
    """
    建物
    """
    template_name = 'building/building.html'

    def __init__(self, **kwargs):
        self.user = None
        self.building = None

        super().__init__(**kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        if not self.user:
            raise Http404

        oid = kwargs['oid']
        conditions = Q(oid=oid, is_deleted=False)
        if self.user.is_trader:
            conditions.add(Q(is_hidden_vacancy=False), Q.AND)   # 非表示分は対象外
        self.building = get_object_or_404(Building, conditions)

        self.building.auth_user = self.user

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['company'] = Company.get_instance()
        context['building'] = self.building
        context['condo_fees_name'] = settings.CONDO_FEES_NAME

        return context
