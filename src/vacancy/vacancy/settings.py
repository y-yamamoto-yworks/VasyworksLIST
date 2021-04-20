"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '任意のキー'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'django_filters',
    'api',
    'building',
    'documents',
    'garage',
    'menu',
    'movie',
    'panorama',
    'rent_db',
    'room',
    'users',
    'viewer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vacancy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vacancy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rent_db',
        'USER': 'yworks',
        'PASSWORD': '任意のパスワード',
        'HOST': 'DBサーバのIPアドレスなど',
        'PORT': '5432',
    }
}


# Authorization
AUTH_USER_MODEL = 'users.VacancyUser'
AUTHENTICATION_BACKENDS = [
    'users.backends.UserBackEnd',
]
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/menu/'
LOGIN_ERROR_URL = '/login/'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Humanize
NUMBER_GROUPING = 3


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Application settings
COMPANY_ID = 1      # 会社ID（会社マスタ参照用）
DISPLAY_INFO_DATE = False   # お知らせの日付表示
DEFAULT_PREF_ID = 26        # デフォルトの都道府県ID（未指定可）
INCLUDE_NO_ROOM_BUILDINGS = True     # 自社ユーザの時に居住用一覧で空き無し物件を含む場合はTrue
BUILDING_LIST_PAGE_SIZE = 10        # 建物リストのページサイズ
ROOM_LIST_PAGE_SIZE = 50      # 部屋リストのページサイズ
CONDO_FEES_NAME = '共益費'         # 共益費項目の表示名（共益費または管理費）
CACHE_FILE_URL = '/viewer/cache_media/'       # キャッシュファイルのURL
CACHE_FILE_DIR = os.path.join(BASE_DIR, 'media', 'cache')      # キャッシュファイルのディレクトリ
ORIGINAL_FILE_DIR = os.path.join(BASE_DIR, 'media', 'public')       # オリジナルファイルのディレクトリ
WATER_MARK_FONT_SIZE = 32   # キャッシュ画像の透かしのフォントサイズ
WATER_MARK_OPACITY = 64     # キャッシュ画像の透かしの不透明度
ORIGINAL_IMAGE_SIZE = 1920      # オリジナルキャッシュ画像の最大サイズ
THUMBNAIL_IMAGE_SIZE = 240      # サムネイルキャッシュ画像の最大サイズ
SMALL_IMAGE_SIZE = 320      # 小キャッシュ画像の最大サイズ
MEDIUM_IMAGE_SIZE = 640     # 中キャッシュ画像の最大サイズ
LARGE_IMAGE_SIZE = 1280     # 大キャッシュ画像の最大サイズ
SMALL_IMAGE_LEVEL = 2       # 小キャッシュ画像を表示させるユーザレベル下限
MEDIUM_IMAGE_LEVEL = 3       # 中キャッシュ画像を表示させるユーザレベル下限
LARGE_IMAGE_LEVEL = 5       # 大キャッシュ画像を表示させるユーザレベル下限
STANDARD_AUTH_LEVEL = 3     # 標準の部屋閲覧レベル（建物リストでの色分け表示用）
