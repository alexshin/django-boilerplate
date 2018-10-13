import json

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

from guardian.shortcuts import remove_perm

from ...utils import send_verification_code, send_password_recovery_code

User = get_user_model()


class UserTestCase(APITestCase):

    def setUp(self):
        self.credentials = {
            'username': 'somebody@example.com',
            'password': 'q1w2e3r4t5y6'
        }

        self.user = User.objects.create_user(**self.credentials)

    def _get_token_response(self):
        return self.client.post('/api/v1/users/token/',
                                data=json.dumps(self.credentials),
                                content_type='application/json')

    def test_obtaining_token(self):
        response = self._get_token_response()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get('token', False) != False)

    def test_me_endpoint(self):
        response = self._get_token_response()
        token = response.data.get('token')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        me_response = client.get('/api/v1/users/me', content_type='application/json')

        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.data.get('email'), self.credentials.get('username'))


class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user(password='testpassword', email='test@example.com')

        # URL for creating an account.
        self.create_url = reverse('api-v1-user-register')
        self.email_confirm_url = reverse('api-v1-user-confirm-email')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }

        response = self.client.post(self.create_url, data, format='json')

        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

    def test_create_user_with_short_password(self):
        """
        Ensure user is not created for password lengths less than 8.
        """
        data = {
            'email': 'foobarbaz@example.com',
            'password': 'foo'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
            'email': 'foobarbaz@example.com',
            'password': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
            'email': 'test@example.com',
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'email': 'testing',
            'passsword': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        data = {
            'email': '',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['email']), 1)

    def test_authenticated_user(self):
        data = {
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }
        token = Token.objects.create(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def _get_context_and_token(self):
        context = send_verification_code(user=self.test_user, password='somepassword')
        token = context.get('token')
        self.assertTrue(token in context.get('link'))

        return context, token

    def test_email_confirmation_wrong_code(self):
        context, token = self._get_context_and_token()

        # Wrong token
        data = {
            'user_id': str(context.get('user').pk),
            'code': 'something-without-sense'
        }
        response = self.client.post(self.email_confirm_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_confirmation_wrong_user(self):
        context, token = self._get_context_and_token()

        # Wrong user
        data = {
            'user_id': '999',
            'code': token
        }
        response = self.client.post(self.email_confirm_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_confirmation_ok(self):
        context, token = self._get_context_and_token()

        # Everything is OK
        data = {
            'user_id': str(context.get('user').pk),
            'code': token
        }

        response = self.client.post(self.email_confirm_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(self.test_user.groups.filter(name='USER').exists())
        self.assertFalse(self.test_user.groups.filter(name='NOT_VERIFIED_USER').exists())

        self.assertFalse(self.test_user.has_perm('user.validate_email', self.test_user))

    def test_email_confirmation_empty_perms(self):
        context, token = self._get_context_and_token()

        remove_perm('user.validate_email', self.test_user, self.test_user)

        # Everything is OK
        data = {
            'user_id': str(context.get('user').pk),
            'code': token
        }
        response = self.client.post(self.email_confirm_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordRecoveryTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(password='testpassword', email='recovery@example.com')

        # URLs for password recovery.
        self.password_recovery_url = reverse('api-v1-user-request-password-recovery')
        self.password_recovery_confirm_url = reverse('api-v1-user-confirm-password-recovery')

    def _get_context_and_token(self):
        context = send_password_recovery_code(user=self.test_user)
        token = context.get('token')
        self.assertTrue(token in context.get('link'))

        return context, token

    def test_password_recovery_request(self):
        data = {'email': 'recovery@example.com'}

        response = self.client.post(self.password_recovery_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])

    def test_password_recovery_request_with_nonexistent_email(self):
        data = {'email': 'some@nonexistent.email'}

        response = self.client.post(self.password_recovery_url, data, format='json')

        # User with current email doesn't exist
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['email']), 1)

    def test_password_recovery_request_with_empty_email(self):
        data = {'email': ''}

        response = self.client.post(self.password_recovery_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['email']), 1)

    def test_password_recovery_confirmation(self):
        context, token = self._get_context_and_token()
        data = {
            'id': str(context.get('user').pk),
            'code': token,
            'password': 'SoMeVal1DPassword',
            'password_confirmation': 'SoMeVal1DPassword'
        }

        old_password = self.test_user.password

        response = self.client.post(self.password_recovery_confirm_url, data, format='json')

        new_password = User.objects.get(id=data.get('id'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(old_password, new_password)

    def test_password_recovery_confirmation_with_invalid_password(self):
        context, token = self._get_context_and_token()
        data = {
            'id': str(context.get('user').pk),
            'code': token,
            'password': '1',
            'password_confirmation': '1'
        }

        response = self.client.post(self.password_recovery_confirm_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['password']), 1)

    def test_password_recovery_confirmation_with_invalid_confirmation(self):
        context, token = self._get_context_and_token()
        data = {
            'id': str(context.get('user').pk),
            'code': token,
            'password': 'SoMeVal1DPassword',
            'password_confirmation': 'SoMeINVal1DPassword'
        }

        response = self.client.post(self.password_recovery_confirm_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['non_field_errors']), 1)

