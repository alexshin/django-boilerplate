from django.contrib.auth import get_user_model
from django.conf import settings

SUPERUSER_USER_NAME = settings.SUPERUSER_USER_NAME

User = get_user_model()


def apply():
    User = get_user_model()
    User.objects.create_superuser(email=SUPERUSER_USER_NAME, password='q1w2e3r4t5y6')