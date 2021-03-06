from typing import List
from ..shared import *

DEBUG = False
ALLOWED_HOSTS: List[str] = []

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b=c(untxoz5s!9sudc9u!)b%(w=029(0d2pzodl04m(3x35e=l'

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

CORS_ORIGIN_ALLOW_ALL = True
