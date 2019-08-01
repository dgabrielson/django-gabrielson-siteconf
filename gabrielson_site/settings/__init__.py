# Django settings for the gabrielson.ca site project.

# A note about paths in this file:  In order to provide a valid
# initial config, all paths in this file are set to /dev/null/blah.
# Defining a reasonable gabrielson_site.conf.json is described at the
# end of this file.

import os

from django.conf.global_settings import *
from django.urls import reverse_lazy

from .load_json_conf import json_conf
from .logging import LOGGING
from .post_local import finalize_settings

del DEFAULT_CONTENT_TYPE  # remove in Django 3.0

DEBUG = True

ADMINS = (("Dave Gabrielson", "dave@gabrielson.ca"),)

MANAGERS = ADMINS

# a dev default database
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "/dev/null/data.db"}
}

SITE_ID = 1
TIME_ZONE = "America/Winnipeg"
USE_TZ = True
LANGUAGE_CODE = "en-us"
USE_I18N = False
ROOT_URLCONF = "gabrielson_site.urls"
WSGI_APPLICATION = "gabrielson_site.wsgi.application"
"""
$ ./manage.py shell
from django.utils.crypto import get_random_string ;\
chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)" ;\
print "SECRET_KEY = {0!r}".format(get_random_string(50, chars))
"""
SECRET_KEY = "this-is-my-secret-key_(actually-set-in-local_settings.py)"

# MEDIA: uploaded files
MEDIA_ROOT = "/dev/null/media"
MEDIA_URL = "/media/"
# STATIC FILES: non-dynamic assets {css,img,js}
STATIC_URL = "/static/"
STATIC_ROOT = "/dev/null/static"
STATICFILES_DIRS = []

INSTALLED_APPS = (
    "site_templates",
    "gabrielson_responsive",
    "flat_responsive",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "xkcd",
    "aquainfo",
    #    'scrapbook',
    "diet",
    "markuphelpers",
    #    'asw',
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # insert your TEMPLATE_DIRS here
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # Default::
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # Custom adds::
                "django.template.context_processors.request",
            ]
        },
    }
]

# MIDDLEWARE_CLASSES += (
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'iwebkit.middleware.iOSMiddleware',
#     )

# This is becoming "MIDDLEWARE" (empty by default; use):
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o644

################################################

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

LOGIN_URL = reverse_lazy("site-login")
LOGIN_REDIRECT_URL = reverse_lazy("site-index")
LOGOUT_URL = reverse_lazy("site-logout")

INSTALLED_APPS += ("haystack",)
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": "/dev/null/whoosh_index",
    }
}

################################################
###
### User password strength validation provided by django-passwords
### Wordlist from http://www.openwall.com/wordlists/
###     http://download.openwall.net/pub/wordlists/passwords/password.gz
###     Retrieved: 2013-May-29
###
PASSWORD_MIN_LENGTH = 8
PASSWORD_DICTIONARY = u"/dev/null/words.txt"
PASSWORD_MATCH_THRESHOLD = 0.94
PASSWORD_COMPLEXITY = {  # You can ommit any or all of these for no limit for that particular set
    "UPPER": 1,  # Uppercase
    "LOWER": 1,  # Lowercase
    "DIGITS": 1,  # Digits
    "PUNCTUATION": 1,  # Punctuation (string.punctuation)
    # "NON ASCII": 1,   # Non Ascii (ord() >= 128)
    # "WORDS": 1        # Words (substrings seperates by a whitespace)
}

################################################
################################################
### Finally, load local settings, auto-detect and augment
### STATICFILES_DIRS and TEMPLATE[k]['DIRS']
### with project values; and finalize
### (so the project doesn't also need to be an app)


base_path = os.path.dirname(os.path.dirname(__file__))
project_static = os.path.join(base_path, "static")
if os.path.exists(project_static):
    STATICFILES_DIRS += (project_static,)
project_templates = os.path.join(base_path, "templates")
if os.path.exists(project_templates):
    # TEMPLATE_DIRS += (project_templates, )
    for t in TEMPLATES:
        if "DIRS" in t:
            t["DIRS"].append(project_templates)

locals().update(json_conf())
locals().update(finalize_settings(locals()))

################################################
################################################
