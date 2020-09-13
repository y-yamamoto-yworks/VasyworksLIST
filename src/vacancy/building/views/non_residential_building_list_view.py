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
from api.api_helper import ApiHelper
from rent_db.models import *
from building.forms import SearchBuildingAreaForm


class NonResidentialBuildingListView(FormView):
    """
    非居住建物リスト
    """
    form_class = SearchBuildingAreaForm
    template_name = 'building/non_residential_building_list.html'
    user = None
    pref = None
    city = None
    area = None
    page_number = 1

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        if not self.user:
            raise Http404

        page_number = kwargs.get('page_number')
        if page_number:
            self.page_number = xint(page_number)

        if request.method == 'GET':
            id = request.GET.get('pref', None)
            if id:
                self.pref = Pref.objects.get(pk=id)

            id = request.GET.get('city', None)
            if id:
                self.city = City.objects.get(pk=id)

            id = request.GET.get('area', None)
            if id:
                self.area = Area.objects.get(pk=id)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['company'] = Company.get_instance()
        context['api_key'] = ApiHelper.get_key()

        buildings = Building.search_non_residential(
            self.user,
            self.pref,
            self.city,
            self.area
        )

        if buildings:
            paginator = Paginator(buildings, settings.BUILDING_LIST_PAGE_SIZE)
            page = paginator.get_page(self.page_number)
            context['buildings'] = page
            context['page_base_url'] = reverse_lazy('building_non_residential_building_list')

        params = ''
        if self.city:
            context['default_pref_id'] = self.city.pref.id
            context['default_city_id'] = self.city.id
            params = 'pref={0}&city={1}'.format(self.city.pref.id, self.city.id)

            if self.area:
                context['default_area_id'] = self.area.id
                params += '&area={0}'.format(self.area.id)

        elif self.pref:
            context['default_pref_id'] = self.pref.id
            params = 'pref={0}'.format(self.pref.id)

        elif settings.DEFAULT_PREF_ID:
            context['default_pref_id'] = settings.DEFAULT_PREF_ID

        if params != '':
            context['page_params'] = params

        context['condo_fees_name'] = settings.CONDO_FEES_NAME

        return context

    def form_valid(self, form):
        if self.request.method in ('POST', 'PUT'):
            if form.data.get('pref'):
                data = form.data['pref']
                if data != '0':
                    self.pref = Pref.objects.get(pk=data)
            if form.data.get('city'):
                data = form.data['city']
                if data != '0':
                    self.city = City.objects.get(pk=data)
            if form.data.get('area'):
                data = form.data['area']
                if data != '0':
                    self.area = Area.objects.get(pk=data)

        return self.render_to_response(self.get_context_data())
