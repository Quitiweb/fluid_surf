""" Development settings and globals """

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i52ahg=sxvuw9w9heb#j_-cle!3)z6gg1$pc_s9omkpthw8$8*'

ALLOWED_HOSTS += [
    '127.0.0.1',
    'localhost',
    'fs.quitiweb.com',
]

# To send emails to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
