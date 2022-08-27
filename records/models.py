from typing import List, Optional, Tuple

from django.db import models

from domains.models import Domain
from subdomains.models import Subdomain
from .providers.base import BaseRecordProvider


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
        return self.join_name(self.service, self.protocol, self.name)

    @property
    def data(self) -> str:
        return self.join_data(self.priority, self.weight, self.port, self.target)

    def __str__(self):
        return f'{self.full_name} {self.ttl} IN {self.type} {self.data}'

    @classmethod
    def list_records(cls, provider: Optional[BaseRecordProvider], subdomain: Subdomain) -> List['Record']:
        if provider:
            provider_records = provider.list_records(subdomain.name, subdomain.domain)
            provider_record_id_set = set(map(lambda x: x['provider_id'], provider_records))
            for record in cls.objects.filter(subdomain_name=subdomain.name):
                if record.provider_id not in provider_record_id_set:
                    record.delete()
            for provider_record in provider_records:
                cls.objects.update_or_create(provider_id=provider_record.get('provider_id'), defaults=provider_record)
        return cls.objects.filter(subdomain_name=subdomain.name)

    @classmethod
    def create_record(cls, provider: Optional[BaseRecordProvider], subdomain: Subdomain, **kwargs) -> 'List':
        record = cls(subdomain_name=subdomain.name, domain=subdomain.domain, **kwargs)
        if provider:
            provider_record = provider.create_record(subdomain.name, subdomain.domain, **kwargs)
            record.provider_id = provider_record.get('provider_id')
        return record.save()

    @classmethod
    def retrieve_record(cls, provider: Optional[BaseRecordProvider], subdomain: Subdomain, id: int) -> 'List':
        record = cls.objects.get(subdomain_name=subdomain.name, pk=id)
        if provider:
            provider_record = provider.retrieve_record(subdomain.name, subdomain.domain, record.provider_id)
            for k, v in provider_record.items():
                setattr(record, k, v)
            return record.save()
        return record

    @classmethod
    def update_record(cls, provider: Optional[BaseRecordProvider], subdomain: Subdomain, id: int, **kwargs) -> 'List':
        record = cls.objects.get(subdomain_name=subdomain.name, pk=id)
        for k, v in kwargs.items():
            setattr(record, k, v)
        if provider:
            provider.update_record(subdomain.name, subdomain.domain, record.provider_id, **kwargs)
        return record.save()

    @classmethod
    def delete_record(cls, provider: Optional[BaseRecordProvider], subdomain: Subdomain, id: int) -> None:
        record = cls.objects.get(subdomain_name=subdomain.name, pk=id)
        if provider:
            provider.delete_record(subdomain.name, subdomain.domain, record.provider_id)
        record.delete()

    @classmethod
    def export_zone(cls, provider: Optional[BaseRecordProvider], subdomain: Subdomain) -> str:
        return '\n'.join(map(str, cls.list_records(provider, subdomain)))

    @classmethod
    def import_zone(cls, provider: Optional[BaseRecordProvider], subdomain: Subdomain, zone: str) -> None:
        lines = list(filter(lambda x: x[0] != ';', map(lambda x: x.strip(), zone.splitlines())))
        for line in lines:
            r = line.split()
            service, protocol, name = cls.split_name(r[0])
            priority, weight, port, target = cls.split_data(r[-1])
            kwargs = {
                'name': name,
                'ttl': int(r[1]) if r[1] != 'IN' else int(r[2]),
                'type': r[3],
                'service': service,
                'protocol': protocol,
                'priority': priority,
                'weight': weight,
                'port': port,
                'target': target,
            }
            cls.create_record(provider, subdomain, **kwargs)

    @staticmethod
    def split_name(full_name: str) -> Tuple[Optional[str], Optional[str], str]:
        names = full_name.split('.')
        service = names.pop(0) if names[0].startswith('_') else None
        protocol = names.pop(0) if names[0].startswith('_') else None
        name = '.'.join(names)
        return service, protocol, name

    @staticmethod
    def join_name(service: Optional[str], protocol: Optional[str], name: str) -> str:
        if service is not None and not service.startswith('_'):
            service = '_' + service
        if protocol is not None and not protocol.startswith('_'):
            protocol = '_' + protocol
        return '.'.join(filter(lambda x: x is not None, [service, protocol, name]))

    @staticmethod
    def split_data(data: str) -> Tuple[Optional[int], Optional[int], Optional[int], str]:
        values = data.split()
        priority = int(values[0]) if len(values) > 1 else None
        weight = int(values[1]) if len(values) == 4 else None
        port = int(values[2]) if len(values) == 4 else None
        target = values[-1]
        return priority, weight, port, target

    @staticmethod
    def join_data(priority: Optional[int], weight: Optional[int], port: Optional[int], target: str) -> str:
        return ' '.join(map(str, filter(lambda x: x is not None, [priority, weight, port, target])))
