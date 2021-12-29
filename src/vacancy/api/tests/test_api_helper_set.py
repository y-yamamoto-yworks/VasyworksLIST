"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.test import Client
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
        self.assertEqual(ApiHelper.get_key(), '8e41d5d414744d3bcbafd94c1d24549581cba7543bd0fc0400ce34c7061a3b52248404713402ac04')

    def test_check_key(self):
        self.assertTrue(ApiHelper.check_key('8e41d5d414744d3bcbafd94c1d24549581cba7543bd0fc0400ce34c7061a3b52248404713402ac04'))
