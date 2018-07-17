from django.contrib.auth import get_user_model
from django.conf import settings

from post_office import mail

from .tokens import user_activation_token


User = get_user_model()
BASE_URL = settings.BASE_URL
NOREPLY_EMAIL = settings.NOREPLY_EMAIL


def get_client_ip(request):

    """
    Simple function to return IP address of client
    :param request:
    :return:
    """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_verification_code(user: User, password: str):
    token = user_activation_token.make_token(user=user)
    link = f'{BASE_URL}users/confirm_email/{user.pk}/{token}'

    context = {
        'token': token,
        'link': link,
        'plain_password': password,
        'user': user
    }

    mail.send(
        [user.email],
        NOREPLY_EMAIL,
        template='registration_email_verification',
        context=context
    )

    return context


def send_password_recovery_code(user: User):
    token = user_activation_token.make_token(user=user)
    link = f'{BASE_URL}users/new_password/{user.pk}/{token}'

    context = {
        'token': token,
        'link': link,
        'user': user
    }

    mail.send(
        [user.email],
        NOREPLY_EMAIL,
        template='user_password_recovery',
        context=context
    )

    return context
