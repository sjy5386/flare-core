from domains.models import Domain
from .base import BaseRecordProvider
from .digitalocean import DigitalOceanRecordProvider

PROVIDER_CLASS = DigitalOceanRecordProvider


def get_record_provider(domain: Domain) -> BaseRecordProvider:
    return PROVIDER_CLASS()
