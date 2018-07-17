from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'

    def ready(self):
        from .handlers_perms import add_user_to_base_group, add_user_to_confirmed_group
