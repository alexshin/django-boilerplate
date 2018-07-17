import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.conf import settings
from rest_framework.test import APITestCase, APIClient

USERS = settings.USERS
NOT_VERIFIED_USERS = settings.EMAIL_IS_NOT_VERIFIED_USERS

User = get_user_model()


class AuthorizedAPITestCase(APITestCase):
    def _get_token(self):
        response = self.client.post('/api/v1/user/token/',
                                    data=json.dumps(self.credentials),
                                    content_type='application/json')

        return response.data.get('token')

    def _get_authorized_client(self, token: str = None) -> APIClient:
        if token is None:
            token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        return self.client

    def setUp(self):
        self.credentials = {
            'username': 'somebody@example.com',
            'password': 'q1w2e3r4t5y6'
        }

        self.user = User.objects.create_user(**self.credentials)

        self.user_group = Group.objects.get(name=USERS)
        self.anonymous_group = Group.objects.get(name=NOT_VERIFIED_USERS)

        self.user.groups.clear()
        self.user.groups.add(self.user_group)

        self.client = APIClient()
        self.client = self._get_authorized_client()