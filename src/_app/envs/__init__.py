import os

ENVIRONMENT = os.getenv('APP_ENVIRONMENT', 'dev')

if ENVIRONMENT == 'dev':
    from .dev import *
elif ENVIRONMENT == 'test':
    from .test import *
elif ENVIRONMENT == 'prod':
    from .prod import *
