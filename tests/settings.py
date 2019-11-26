# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import django

# import django_magnificent_messages.constants as message_constants

DEBUG = True
USE_TZ = False


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "8ah(*5$ds!4-284y0shckwgn%uun&5!up#@yz&k(5xs+)2bqlw"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_db.sqlite3",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_magnificent_messages.apps.DjangoMagnificentMessagesConfig",
    "tests"
]

SITE_ID = 1

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django_magnificent_messages.middleware.MessageMiddleware",
)
