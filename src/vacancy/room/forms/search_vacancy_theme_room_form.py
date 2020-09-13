"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
import re
from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rent_db.models import Pref, City, Area


class SearchVacancyThemeRoomForm(forms.Form):
    """
    テーマ別部屋検索フォーム
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['pref'] = forms.ModelChoiceField(
            label=_('都道府県'),
            queryset=Pref.objects.filter(
                Q(is_trading_area=True) | Q(pk=0)
            ).order_by('priority', 'id').all(),
            required=False,
        )
        self.fields['pref'].widget.attrs['v-model'] = 'pref'
        self.fields['pref'].widget.attrs['v-on:change'] = 'changePref($event)'

        self.fields['city'] = forms.ModelChoiceField(
            label=_('市区町村'),
            queryset=City.objects.filter(
                Q(is_trading_area=True, is_stopped=False) | Q(pk=0)
            ).order_by('priority', 'id').all(),
            required=False,
        )
        self.fields['city'].widget.attrs['v-model'] = 'city'
        self.fields['city'].widget.attrs['v-on:change'] = 'changeCity($event)'

        self.fields['area'] = forms.ModelChoiceField(
            label=_('エリア'),
            queryset=Area.objects.filter(
                Q(is_stopped=False) | Q(pk=0)
            ).order_by('kana', 'id').all(),
            required=False,
        )
        self.fields['area'].widget.attrs['v-model'] = 'area'

        for key in self.fields.keys():
            field = self.fields[key]
            field.widget.attrs['ref'] = key
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
