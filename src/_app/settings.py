import os

ENVIRONMENT = os.getenv('APP_ENVIRONMENT', 'dev')

if ENVIRONMENT == 'dev':
    from .env.dev import *
elif ENVIRONMENT == 'test':
    from .env.test import *
elif ENVIRONMENT == 'prod':
    from .env.prod import *
