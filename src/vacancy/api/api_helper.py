"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.utils import timezone
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from lib.convert import *
from lib.functions import *
from rent_db.models import Company


class ApiHelper:
    """APIヘルパークラス"""
    @staticmethod
    def get_key():
        """APIキーの取得"""
        company = Company.objects.get(pk=settings.COMPANY_ID)
        return ApiHelper.get_3des_encrypt(company.api_key, company.internal_api_key)

    @staticmethod
    def check_key(key: str):
        """APIキー確認"""
        ans = False
        company = Company.objects.get(pk=settings.COMPANY_ID)
        if company.api_key == ApiHelper.get_3des_decrypt(key, company.internal_api_key):
            ans = True

        return ans

    @staticmethod
    def get_3des_encrypt(target, crypt_key):
        key = crypt_key.lower()[:24].encode("utf-8")
        iv = crypt_key.lower()[-8:].encode("utf-8")
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        data = pad(str(target).encode("utf-8"), DES3.block_size)
        cipher_text = cipher.encrypt(data)
        return cipher_text.hex()

    @staticmethod
    def get_3des_decrypt(target, crypt_key):
        cipher_text = bytes.fromhex(target)
        key = crypt_key.lower()[:24].encode("utf-8")
        iv = crypt_key.lower()[-8:].encode("utf-8")
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        plain_text = unpad(cipher.decrypt(cipher_text), DES3.block_size)
        return plain_text.decode()
