from .base import *


SECRET_KEY = "django-insecure-#fmhbw7j5=l7f&0w=_$e^f=7n)cs45p$6kte_$bu7v(iu3&haz"

DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS+=['debug_toolbar',]

MIDDLEWARE += [
    
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
