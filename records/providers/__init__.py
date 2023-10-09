import os
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


DEFAULT_RECORD_PROVIDER = os.environ.get('DEFAULT_RECORD_PROVIDER') or RecordProvider.DIGITALOCEAN.name


def get_record_provider(domain: Domain) -> BaseRecordProvider:
    return RecordProvider[DEFAULT_RECORD_PROVIDER].provider_class()
