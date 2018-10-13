from os import path
from django.conf import settings
from pathlib import Path as PathLib

from post_office.models import EmailTemplate

EMAIL_FIXTURES_BASE_DIR = path.join(settings.STATIC_FIXTURES_BASE_DIR, 'emails')


TEMPLATES = [
    {
        'name': 'user_password_recovery',
        'subject': 'Password recovery'
    }, {
        'name': 'registration_email_verification',
        'subject': 'Verify your email',
    }
]


def apply():
    content = {}

    for template in TEMPLATES:
        template_name = template['name']
        template_subject = template['subject']

        for ext in ['html', 'txt']:
            filename = path.join(EMAIL_FIXTURES_BASE_DIR, f'{template_name}.{ext}')

            if path.isfile(filename):
                content[ext] = PathLib(filename).read_text(encoding='utf-8')
            elif path.isfile(filename):
                content[ext] = PathLib(filename).read_text(encoding='utf-8')
            else:
                content[ext] = ''
                print(f'[WARNING] file "{filename}" is missed!')

        EmailTemplate.objects.create(
            name=template_name,
            subject=template_subject,
            content=content.get('txt'),
            html_content=content.get('html'),
        )
