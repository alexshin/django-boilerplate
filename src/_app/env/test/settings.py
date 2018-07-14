from ..common import *


DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'app',
        'USER': 'localroot',
        'PASSWORD': 'localrootpass',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}