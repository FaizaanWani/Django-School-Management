from .base import *
from .base import env


DEBUG = True
SSL_ISSANDBOX = True
ALLOWED_HOSTS = ['*', ]

THIRD_PARTY_APPS += [
    'debug_toolbar',
]
INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Django-Debug-Toolbar
INTERNAL_IPS = ['127.0.0.1', '0.0.0.0', '*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dtq_dev',
        'USER': 'postgres',
        'PASSWORD': '@DTQ#9977',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
