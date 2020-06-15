"""
Django settings for fluidsurf project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_APP_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(PROJECT_APP_ROOT))
HOST_ROOT = os.path.abspath(os.path.dirname(PROJECT_ROOT))
PUBLIC_ROOT = os.path.abspath(os.path.join(HOST_ROOT, 'public'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '.fluidsurf.es',
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

# Application definition

INSTALLED_APPS = [
    'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.forms',
    'tinymce',
    'fluidsurf.apps.users',
    'fluidsurf.apps.payments',
    'fluidsurf.apps.home',
    'fluidsurf.apps.dashboard',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.stripe',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.instagram',
    'localflavor',
    'qr_code',
    'django_social_share',
    'imagekit',
    'django_google_maps',
    'django_filters',
    'braintree',
    'certifi',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'fluidsurf.urls'

AUTH_USER_MODEL = 'users.CustomUser'

# Templates

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates'), 'templates', 'fluidsurf/templates', ],
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

WSGI_APPLICATION = 'fluidsurf.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Allauth access
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 2

SOCIALACCOUNT_PROVIDERS = {
    'stripe': {
        'AUTH_PARAMS': {
            'scope': 'read_write',
        },
    },
}

# Login/logout redirects to homepage
LOGIN_REDIRECT_URL = '/setup'
LOGOUT_REDIRECT_URL = '/login'

SERVER_EMAIL = 'contact@fluidsurf.es'

# Imagen que se pone como marca de agua
WATERMARK_IMAGE = os.path.join(PROJECT_ROOT, 'static/home/img/logo.png')

# API Key para la aplicacion django-google-maps
BING_MAPS_API_KEY = 'Ah53ETOrZ7Pe60kRwxCxtXIItc7a2uTpuR6iWxpW3nFOl96LqDr0-ZVwi_XR5tTu'

STRIPE_SECRET_KEY = 'sk_test_7S7kED02VXdJRZs1wuIeRdev005AjO1bWk'
STRIPE_PUBLISHABLE_KEY = 'pk_test_hDBPIclBeoC9lzWKLmC7qP9T00pifq63fG'
STRIPE_TEST_CLIENT_ID = 'ca_GxnZAsopwVt4CWS0PZl4oUT2nlArkDOi'

GOOGLE_RECAPTCHA_SECRET_KEY = '6LdNpL4UAAAAAF9IgR0Oz-mjlDg3KQKp6RSwxfci'

BRAINTREE_PRODUCTION = False  # Para cambiar entre version live o sandbox
BRAINTREE_MERCHANT_ID = "fjzw2mzxchqc5mc7"
BRAINTREE_PUBLIC_KEY = "xwnbs5cgm8q2jr98"
BRAINTREE_PRIVATE_KEY = "aea75ad6fe613b377999d5c852021e25"

# GeoIP

GEOIP_PATH = os.path.join(PROJECT_ROOT, 'geoip/')