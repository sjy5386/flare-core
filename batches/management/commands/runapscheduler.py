import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore

from base.settings import APPLICATION_TYPE, ApplicationType
from subdomains.jobs import find_expired_subdomains_job


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
        scheduler.add_job(
            find_expired_subdomains_job,
            trigger=CronTrigger(day='*'),
            max_instances=1,
            replace_existing=True,
        )
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
        finally:
            self.logger.info('========== Ending batch application ==========')
