from django.core.management.base import BaseCommand, CommandError

from ...loaders import load


class Command(BaseCommand):
    help = 'Apply fixtures'

    def add_arguments(self, parser):
        parser.add_argument("-f", "--fixtures", dest="fixtures", action="append", help='Fixtures to apply')

    def handle(self, *args, **options):
        if 'fixtures' in options and options['fixtures'] != []:
            load(include_fixtures=options['fixtures'])
        else:
            load()