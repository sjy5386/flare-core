from typing import Optional

from django.db import models

from domains.models import Domain
from subdomains.models import Subdomain
from .providers.base import BaseProvider


class Record(models.Model):
    class RecordType(models.TextChoices):
        A = 'A', 'A - a host address',
        NS = 'NS', 'NS - an authoritative name server',
        CNAME = 'CNAME', 'CNAME - the canonical name for an alias',
        MX = 'MX', 'MX - mail exchange',
        TXT = 'TXT', 'TXT - text strings',
        AAAA = 'AAAA', 'AAAA - IP6 Address',
        SRV = 'SRV', 'SRV - Server Selection'

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    provider_id = models.CharField(max_length=255, unique=True, null=True)

    subdomain_name = models.CharField(max_length=63)
    domain = models.ForeignKey(Domain, on_delete=models.RESTRICT)

    name = models.CharField('Name', max_length=63)
    ttl = models.IntegerField('TTL', default=3600)
    type = models.CharField('Type', max_length=10, choices=RecordType.choices)

    service = models.CharField('Service', max_length=63, null=True, help_text='Required for SRV record.')
    protocol = models.CharField('Protocol', max_length=63, null=True, help_text='Required for SRV record.')

    priority = models.IntegerField('Priority', null=True, help_text='Required for MX and SRV records.')
    weight = models.IntegerField('Weight', null=True, help_text='Required for SRV record.')
    port = models.IntegerField('Port', null=True, help_text='Required for SRV record.')

    target = models.CharField('Target', max_length=255)

    @property
    def full_name(self) -> str:
        name = f'{self.name}.{self.subdomain_name}.{self.domain.name}'
        return name if self.type != 'SRV' else f'{self.service}.{self.protocol}.{name}'

    @property
    def data(self) -> str:
        return f'{self.priority} {self.weight} {self.port} {self.target}'.strip()

    def __str__(self):
        return f'{self.full_name} {self.ttl} IN {self.type} {self.data}'

    @classmethod
    def list_records(cls, provider: Optional[BaseProvider], subdomain: Subdomain):
        if provider:
            return provider.list_records(subdomain)
        return cls.objects.filter(subdomain_name=subdomain.name)

    @classmethod
    def create_record(cls, provider: Optional[BaseProvider], subdomain: Subdomain, **kwargs):
        record = cls(**kwargs)
        if provider:
            provider.create_record(subdomain, record)
        return record.save()

    @classmethod
    def retrieve_record(cls, provider: Optional[BaseProvider], subdomain: Subdomain, id: int):
        record = cls.objects.get(subdomain_name=subdomain.name, pk=id)
        if provider:
            return provider.retrieve_record(subdomain, record.provider_id)
        return record

    @classmethod
    def update_record(cls, provider: Optional[BaseProvider], subdomain: Subdomain, id: int, **kwargs):
        record = cls.objects.get(subdomain_name=subdomain.name, pk=id)
        for k, v in kwargs.items():
            setattr(record, k, v)
        if provider:
            provider.update_record(subdomain, record.provider_id, record)
        return record.save()

    @classmethod
    def delete_record(cls, provider: Optional[BaseProvider], subdomain: Subdomain, id: int):
        record = cls.objects.get(subdomain_name=subdomain.name, pk=id)
        if provider:
            provider.delete_record(subdomain, record.provider_id)
        record.delete()
