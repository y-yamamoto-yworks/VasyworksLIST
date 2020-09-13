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
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from dateutil.relativedelta import relativedelta
from PIL import Image
from lib.convert import *
from rent_db.models import *
from building.forms import SearchBuildingNameForm


class SearchNameBuildingListView(FormView):
    """
    名称検索建物リスト
    """
    form_class = SearchBuildingNameForm
    template_name = 'building/search_name_building_list.html'
    user = None
    building_name = None
    page_number = 1

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        if not self.user:
            raise Http404

        if request.method == 'GET':
            self.building_name = request.GET.get('name', None)

        page_number = kwargs.get('page_number')
        if page_number:
            self.page_number = xint(page_number)

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['building_name'] = self.building_name
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['company'] = Company.get_instance()

        if self.building_name:
            context["is_searched"] = True
            buildings = Building.search_with_building_name(self.building_name, self.user)
            if buildings:
                paginator = Paginator(buildings, settings.BUILDING_LIST_PAGE_SIZE)
                page = paginator.get_page(self.page_number)
                context['buildings'] = page
                context['page_base_url'] = reverse_lazy('building_search_name_building_list')

            context['default_building_name'] = self.building_name

        else:
            context["is_searched"] = False
            context['buildings'] = None

        context['condo_fees_name'] = settings.CONDO_FEES_NAME

        return context

    def form_valid(self, form):
        if self.request.method in ('POST', 'PUT'):
            if form.data['building_name']:
                self.building_name = form.data['building_name']

        return self.render_to_response(self.get_context_data())
