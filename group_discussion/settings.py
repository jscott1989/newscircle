"""
Django settings for group_discussion project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import django.conf.global_settings as DEFAULT_SETTINGS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&q*s@ylz=!=bei-+p5xh3#+f6z#0cbgobgtc+bno57iv-purgi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG") == "True"

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'compressor',
    'rest_framework',
    'sekizai',
    'foundationform',
    'markdown_deux',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.google',


    'group_discussion',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'group_discussion.urls'

WSGI_APPLICATION = 'group_discussion.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'sekizai.context_processors.sekizai',

    # Required by allauth template tags
    "django.core.context_processors.request",

    # allauth specific context processors
    # "allauth.account.context_processors.account",
    # "allauth.socialaccount.context_processors.socialaccount",

    "group_discussion.context_processors.settings",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'bower_components'),
)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/jsx', 'jsx'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'compiled_static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


REST_FRAMEWORK = {
    'PAGE_SIZE': 100000
}

SITE_ID = 1

ALLOW_AUTHENTICATION = True

ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = "/"

# TODO: real email backend
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Using SENDGRID
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
    EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True


# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config(default="sqlite:/db.sqlite3")

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

EMBEDLY_KEY = "d19f3b97efcb444ca53c335ede44a7ba"

import re

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
#             "link-patterns": [
#     (re.compile(r'(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*[^ \<]*[^ \<\.])(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)', re.IGNORECASE | re.DOTALL), r'\2'),
#     (re.compile(r'(^|[\n ])(((www|ftp)\.[\w\#$%&~.\-;:=,?@\[\]+]*[^ \<]*[^ \<\.])(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)', re.IGNORECASE | re.DOTALL), r'http://\2')
# ]
        },
        "safe_mode": "escape",
    },
}