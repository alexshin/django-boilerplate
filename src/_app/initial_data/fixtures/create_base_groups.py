from django.contrib.auth.models import Group
from django.conf import settings


GROUPS = settings.GROUPS

def apply():
    for g in GROUPS:
        Group.objects.create(name=g)
