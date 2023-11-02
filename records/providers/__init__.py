import os
from enum import Enum

from domains.models import Domain
from .base import BaseDnsRecordProvider
from .digitalocean import DigitalOceanDnsRecordProvider
from .linode import LinodeDnsRecordProvider
from .vultr import VultrDnsRecordProvider


class DnsRecordProvider(Enum):
    DIGITALOCEAN = (DigitalOceanDnsRecordProvider,)
    LINODE = (LinodeDnsRecordProvider,)
    VULTR = (VultrDnsRecordProvider,)

    def __init__(self, provider_class: type[BaseDnsRecordProvider]):
        self.provider_class = provider_class


DEFAULT_DNS_RECORD_PROVIDER = os.environ.get('DEFAULT_DNS_RECORD_PROVIDER') or DnsRecordProvider.DIGITALOCEAN.name


def get_dns_record_provider(domain: Domain) -> BaseDnsRecordProvider:
    return DnsRecordProvider[domain.dns_record_provider].provider_class()
