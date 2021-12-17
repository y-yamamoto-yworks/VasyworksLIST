"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.db import transaction
from rent_db.models import AdType
import warnings


class AdTypeModelTest(TestCase):
    """
    広告種別モデルのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')

        if transaction.get_autocommit():
            transaction.set_autocommit(False)

    def tearDown(self):
        transaction.rollback()

    def test_is_money(self):
        self.assertFalse(AdType.objects.get(pk=0).is_money)
        self.assertFalse(AdType.objects.get(pk=1).is_money)
        self.assertTrue(AdType.objects.get(pk=2).is_money)
        self.assertFalse(AdType.objects.get(pk=3).is_money)

    def test_is_month(self):
        self.assertFalse(AdType.objects.get(pk=0).is_month)
        self.assertFalse(AdType.objects.get(pk=1).is_month)
        self.assertFalse(AdType.objects.get(pk=2).is_month)
        self.assertTrue(AdType.objects.get(pk=3).is_month)

    def test_is_unknown(self):
        self.assertTrue(AdType.objects.get(pk=0).is_unknown)
        self.assertFalse(AdType.objects.get(pk=1).is_unknown)
        self.assertFalse(AdType.objects.get(pk=2).is_unknown)
        self.assertFalse(AdType.objects.get(pk=3).is_unknown)
