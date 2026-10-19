"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.test import Client
from django.test import RequestFactory
from django.urls import reverse
import warnings
from api.api_helper import ApiHelper


class ApiHelperTest(TestCase):
    """
    APIヘルパーのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

    def test_get_key(self):
        self.assertEqual(ApiHelper.get_key(), 'd2bc3da12c8c891681da44440d78bb1a3d16e5f649740fd16aa3b4e1fd7ee540d0a2b2b3fb99325e81b745a1308049e1')

    def test_check_key(self):
        factory = RequestFactory()
        request_valid = factory.get('/', HTTP_X_API_KEY=ApiHelper.get_key())
        self.assertTrue(ApiHelper.check_key(request_valid))

        request_invalid = factory.get('/', HTTP_X_API_KEY='invalid_key')
        self.assertFalse(ApiHelper.check_key(request_invalid))
        