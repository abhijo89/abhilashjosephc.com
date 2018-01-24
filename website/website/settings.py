"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from configparser import RawConfigParser
from inspect import currentframe, getframeinfo
from pathlib import Path

import raven

filename = getframeinfo(currentframe()).filename
root_dir = Path(filename).resolve().parents[2]
config_file = f'{root_dir}/application.cfg'

config = RawConfigParser()
config.read_file(open(config_file))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%3x24@875l5acz_ltl!%g_*o)9adl29326-ej4(t6uq4!jpl!5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'raven.contrib.django.raven_compat',
    'blog',
    'accounts',
    'oauth',
    'comments',
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

ROOT_URLCONF = 'website.urls'
AUTH_USER_MODEL = 'accounts.BlogUser'
LOGIN_URL = '/login/'
SITE_NAME = 'Blog'
SITE_URL = 'https://blog.abhilashjosephc.com'
SITE_DESCRIPTION = 'Abhilash Joseph Blog'
SITE_SEO_DESCRIPTION = 'Abhilash Joseph Blog'
SITE_SEO_KEYWORDS = 'linux,apache,mysql,ubuntu,shell,web,csharp,.net,asp,mac,swift,python,django'
ARTICLE_SUB_LENGTH = 300
SHOW_GOOGLE_ADSENSE = False
PAGINATE_BY = 10
CACHE_CONTROL_MAX_AGE = 2592000
# cache setting
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'djangoblog',
        'TIMEOUT': 60 * 60 * 10
    },
    'locmemcache': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 10800,
        'LOCATION': 'unique-snowflake',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), '..', 'templates'),
        ],
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

OAHUTH = {
    'sina': {
        'appkey': os.environ.get('SINA_APP_KEY'),
        'appsecret': os.environ.get('SINA_APP_SECRET'),
        'callbackurl': 'https://blog.abhilashjosephc.com/oauth/authorize?type=weibo'
    },
    'google': {
        'appkey': os.environ.get('GOOGLE_APP_KEY'),
        'appsecret': os.environ.get('GOOGLE_APP_SECRET'),
        'callbackurl': 'https://blog.abhilashjosephc.com/oauth/authorize?type=google'
    },
    'github': {
        'appkey': os.environ.get('GITHUB_APP_KEY'),
        'appsecret': os.environ.get('GITHUB_APP_SECRET'),
        'callbackurl': 'https://blog.abhilashjosephc.com/oauth/authorize?type=github'
    },
    'facebook': {
        'appkey': os.environ.get('FACEBOOK_APP_KEY'),
        'appsecret': os.environ.get('FACEBOOK_APP_SECRET'),
        'callbackurl': 'https://blog.abhilashjosephc.com/oauth/authorize?type=facebook'
    }
}
SITE_ID = 1

WSGI_APPLICATION = 'website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), '..', 'static')
RAVEN_CONFIG = {
    'dsn': config.get('sentry', 'dsn'),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}
