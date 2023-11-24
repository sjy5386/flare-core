import logging

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Runs APScheduler.'
    logger = logging.getLogger()

    def handle(self, *args, **options):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('========== Starting batch application ==========')
