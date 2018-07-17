from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from .managers import UserManager
from .signals import user_email_confirmed


ANONYMOUS_USER_NAME = settings.ANONYMOUS_USER_NAME


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_email_confirmed = models.BooleanField(
        _('email is activated'),
        default=False,
        help_text=_('Is email activated or not')
    )
    is_game_owner = models.BooleanField(_('user is game owner'), default=False, null=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def confirm_email(self):
        """
        Confirm email automatically
        :return:
        """
        user_email_confirmed.send(sender=User, user=self, code='')
        return self

    @property
    def is_anonymous(self):
        return self.email == ANONYMOUS_USER_NAME

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        permissions = (
            ('validate_email', _('Can validate email')),
            ('change_email', _('Can change email')),
            ('change_password', _('Can change password')),
        )