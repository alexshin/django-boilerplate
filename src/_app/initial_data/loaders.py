from typing import Iterable

# Since Python 3.5 lists in Python is orderable
fixtures = [
    'create_base_groups',
    'user_create_superuser',
    'create_email_templates'
]


def load(include_fixtures: Iterable = None, *args, **kwargs):
    """
    Loads fixtures. If include_fixtures is empty, all fixtures will be loaded and applied
    :param include_fixtures:
    :param args:
    :param kwargs:
    :return:
    """
    fixs = include_fixtures if include_fixtures is not None else fixtures
    for f in fixs:
        d = __import__(f'_app.initial_data.fixtures.{f}', globals(), locals(), ['apply'], 0)
        s = f'[*] Applying fixture {f}: %s'
        try:
            d.apply()
            print(s % 'OK')
        except Exception as e:
            print(s % 'ERROR')
            raise e