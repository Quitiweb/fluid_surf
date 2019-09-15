""" Production settings and globals """

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS += [
    '.kradleco.com',
]

# To send emails using SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = 'contact@kradleco.es'
ADMINS = (('Rafael Ruiz', 'rafa@quitiweb.com'),)
EMAIL_HOST = 'smtp.dreamhost.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'contact@kradleco.es'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')
