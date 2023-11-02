import os
from enum import Enum

from domains.models import Domain
from .base import BaseDnsRecordProvider
from .digitalocean import DigitalOceanDnsRecordProvider
from .linode import LinodeDnsRecordProvider
from .vultr import VultrDnsRecordProvider


class RecordProvider(Enum):
    DIGITALOCEAN = (DigitalOceanDnsRecordProvider,)
    LINODE = (LinodeDnsRecordProvider,)
    VULTR = (VultrDnsRecordProvider,)

    def __init__(self, provider_class: type[BaseDnsRecordProvider]):
        self.provider_class = provider_class


DEFAULT_RECORD_PROVIDER = os.environ.get('DEFAULT_RECORD_PROVIDER') or RecordProvider.DIGITALOCEAN.name


def get_record_provider(domain: Domain) -> BaseDnsRecordProvider:
    return RecordProvider[DEFAULT_RECORD_PROVIDER].provider_class()
