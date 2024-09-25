import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore

from base.settings import APPLICATION_TYPE, ApplicationType
from subdomains.jobs import find_expired_subdomains_job

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Runs APScheduler.'

    def handle(self, *args, **options):
        log.info('========== Starting batch application ==========')
        if APPLICATION_TYPE != ApplicationType.BATCH:
            log.warning('APPLICATION_TYPE is not BATCH.')
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
            log.info('========== Ending batch application ==========')
