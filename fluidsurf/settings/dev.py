""" Development settings and globals """

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i52ahg=sxvuw9w9heb#j_-cle!3)z6gg1$pc_s9omkpthw8$8*'

ALLOWED_HOSTS += [
    '127.0.0.1',
    'localhost',
    '.qw-test.club',
    'fluidsurf-grego.es',
    '192.168.1.21',
    '192.168.1.36',
]


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'fluidsurf',
#         'USER': 'diegea',
#         'PASSWORD': 'HdByaNYk',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# To send emails to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# Stripe
STRIPE_SECRET_KEY = 'sk_test_nWEFMX7XIFMsyDgsrHBxjKkH00DQyr0ykP'
STRIPE_PUBLISHABLE_KEY = 'pk_test_53ciwitrIAzUGwCncznmkxWN00CYFVxjyL'
STRIPE_CONNECT_CLIENT_ID = 'ca_EzcfVzY6Cq9fbjFHIqyskLriYDIM8grD'
