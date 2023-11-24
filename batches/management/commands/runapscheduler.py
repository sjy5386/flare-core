import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore

from base.settings import APPLICATION_TYPE, ApplicationType


class Command(BaseCommand):
    help = 'Runs APScheduler.'
    logger = logging.getLogger()

    def handle(self, *args, **options):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('========== Starting batch application ==========')
        if APPLICATION_TYPE != ApplicationType.BATCH:
            self.logger.warning('APPLICATION_TYPE is not BATCH.')
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
        finally:
            self.logger.info('========== Ending batch application ==========')
