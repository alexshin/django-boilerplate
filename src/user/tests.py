from django.test import TestCase
from django.contrib.auth import get_user_model

from django.conf import settings


class UserTestCase(TestCase):

    def test_anonymous_user_should_exist(self):
        User = get_user_model()   # pylint: disable=invalid-name
        anon = User.get_anonymous()

        self.assertTrue(anon.is_anonymous,
                        msg=f'Anonymous user should exist and his/her name should be {settings.ANONYMOUS_USER_NAME}')

    def test_admin_user_should_exist(self):
        User = get_user_model()   # pylint: disable=invalid-name
        admin = User.objects.filter(is_staff=True, is_active=True)

        self.assertTrue(admin.exists(), msg='There should be at least one superuser')