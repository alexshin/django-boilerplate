from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings

from guardian.shortcuts import assign_perm, remove_perm


SUPERUSER_USER_NAME = settings.SUPERUSER_USER_NAME
GROUPS = settings.GROUPS

from .signals import user_registered, user_email_confirmed

"""
It's not a good idea to assign users here because hard binding,
but ability to manage all assignments in one place is a trade-off
"""

User = get_user_model()


@receiver(user_registered)
def add_user_to_base_group(sender, user: User, plain_password: str, **kwargs):
    if not user.is_anonymous and not user.email == SUPERUSER_USER_NAME:
        group = Group.objects.get(name=settings.EMAIL_IS_NOT_VERIFIED_USERS)
        user.groups.add(group)

        assign_perm('user.validate_email', user, obj=user)


@receiver(user_email_confirmed)
def add_user_to_confirmed_group(sender, user: User, code: str, **kwargs):
    verified_group = Group.objects.get(name=settings.USERS)
    not_verified_group = Group.objects.get(name=settings.EMAIL_IS_NOT_VERIFIED_USERS)

    user.is_email_confirmed = True
    user.save()

    user.groups.remove(not_verified_group)
    user.groups.add(verified_group)

    if not user.email == SUPERUSER_USER_NAME:
        remove_perm('user.validate_email', user, obj=user)
        assign_perm('user.change_password', user, obj=user)