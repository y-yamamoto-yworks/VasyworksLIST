"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.db import transaction
from rent_db.models import DocumentFile
import warnings


class DocumentFileModelTest(TestCase):
    """
    書類ファイルのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')

        if transaction.get_autocommit():
            transaction.set_autocommit(False)

    def tearDown(self):
        transaction.rollback()

    def test_document_file_cache_file_url(self):
        file = DocumentFile.objects.get(pk=1)       # 書類サンプル1
        self.assertEqual(
            file.cache_file_url,
            '/viewer/cache_media/documents/' + file.cache_name,
        )
