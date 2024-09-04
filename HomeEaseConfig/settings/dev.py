from .base import *


SECRET_KEY = "django-insecure-#fmhbw7j5=l7f&0w=_$e^f=7n)cs45p$6kte_$bu7v(iu3&haz"

DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS += ['debug_toolbar', 'drf_spectacular',]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DOMAIN = ('localhost:8000')
SITE_NAME = ('HomeEase')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 2525
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'noreply@homeease.io'
