from enum import Enum

from domains.models import Domain
from .base import BaseRecordProvider
from .digitalocean import DigitalOceanRecordProvider
from .linode import LinodeRecordProvider
from .vultr import VultrRecordProvider


class RecordProvider(Enum):
    DIGITALOCEAN = (DigitalOceanRecordProvider,)
    LINODE = (LinodeRecordProvider,)
    VULTR = (VultrRecordProvider,)

    def __init__(self, provider_class: type[BaseRecordProvider]):
        self.provider_class = provider_class


PROVIDER_CLASS = RecordProvider.DIGITALOCEAN.provider_class


def get_record_provider(domain: Domain) -> BaseRecordProvider:
    return PROVIDER_CLASS()
