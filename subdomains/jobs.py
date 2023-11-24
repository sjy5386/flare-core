import datetime
import logging

from .models import Subdomain


def find_expired_subdomains_job():
    logger = logging.getLogger('find_expired_subdomains_job')
    subdomains = Subdomain.objects.filter(
        expiry__range=(
            datetime.datetime.min.replace(tzinfo=datetime.timezone.utc),
            datetime.datetime.now(tz=datetime.timezone.utc)
        )
    )
    for subdomain in subdomains:
        if not subdomain.has_expired():
            continue
        logger.info(f'{subdomain} has expired at {subdomain.expiry}.')
