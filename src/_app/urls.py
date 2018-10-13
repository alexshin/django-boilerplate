from django.conf import settings

env = settings.ENVIRONMENT

if env == 'prod':
    from .envs.prod.urls import APPLICATION_URLS
elif env == 'test':
    from .envs.test.urls import APPLICATION_URLS
elif env == 'dev':
    from .envs.dev.urls import APPLICATION_URLS
else:
    from .envs.shared.urls import APPLICATION_URLS

urlpatterns = APPLICATION_URLS
