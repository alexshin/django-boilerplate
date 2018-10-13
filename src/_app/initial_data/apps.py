from django.apps import AppConfig
from django.conf import settings

ENVIRONMENT = settings.ENVIRONMENT


class InitialDataConfig(AppConfig):
    name = '_app.initial_data'

    def ready(self):
        # We have to apply fixtures automatically only in test environment
        if ENVIRONMENT == 'test':
            from django.db.models.signals import post_migrate
            from .loaders import load
            post_migrate.connect(load, sender=self)
