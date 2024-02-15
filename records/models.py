import logging
from typing import Any

import uuid
from django.core.cache import cache
from django.db import models

from domains.models import Domain
from subdomains.models import Subdomain
from .exceptions import DnsRecordBadRequestError, DnsRecordNotFoundError, DnsRecordProviderError
from .providers.base import BaseDnsRecordProvider


class Record(models.Model):
    class RecordType(models.TextChoices):
        A = 'A', 'A - a host address',
        NS = 'NS', 'NS - an authoritative name server',
        CNAME = 'CNAME', 'CNAME - the canonical name for an alias',
        MX = 'MX', 'MX - mail exchange',
        TXT = 'TXT', 'TXT - text strings',
        AAAA = 'AAAA', 'AAAA - IP6 Address',
        SRV = 'SRV', 'SRV - Server Selection'

    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=False)
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

    @property
    def subdomain(self) -> Subdomain:
        return Subdomain.objects.get(name=self.subdomain_name, domain=self.domain)

    @property
    def subdomain_uuid(self) -> str:
        return self.subdomain.uuid

    @subdomain_uuid.setter
    def subdomain_uuid(self, value: str) -> None:
        self.subdomain_name = Subdomain.objects.get(uuid=value).name

    @property
    def domain_uuid(self) -> str:
        return self.domain.uuid

    @domain_uuid.setter
    def domain_uuid(self, value: str) -> None:
        self.domain = Domain.objects.get(uuid=value)

    @property
    def domain_name(self) -> str:
        return self.domain.name

    def __str__(self):
        return f'{self.full_name} {self.ttl} IN {self.type} {self.data}'

    @classmethod
    def list_dns_records(cls, provider: BaseDnsRecordProvider | None, subdomain: Subdomain) -> list['Record']:
        if subdomain is None:
            return []
        cache_key = 'dns_records:' + str(subdomain)
        cache_value = cache.get(cache_key)
        if cache_value is not None:
            return cache_value
        if provider:
            try:
                provider_dns_records = provider.list_dns_records(subdomain.name, subdomain.domain)
                provider_dns_record_id_set = set(map(lambda x: x['provider_id'], provider_dns_records))
                for dns_record in cls.objects.filter(subdomain_name=subdomain.name):
                    if dns_record.provider_id not in provider_dns_record_id_set:
                        dns_record.delete()
                dns_record_dict = {provider_id: x for provider_id, x in
                                   map(lambda x: (x.provider_id, x), cls.objects.filter(subdomain_name=subdomain.name))}
                for provider_dns_record in provider_dns_records:
                    provider_id = provider_dns_record.get('provider_id')
                    if provider_id in dns_record_dict:
                        dns_record_dict.get(provider_id).update_by_provider_dns_record(provider_dns_record)
                        continue
                    provider_dns_record.update({
                        'subdomain_name': subdomain.name,
                        'domain': subdomain.domain,
                    })
                    cls.objects.update_or_create(provider_id=provider_id, defaults=provider_dns_record)
            except DnsRecordProviderError as e:
                logging.error(e)
        dns_records = cls.objects.filter(subdomain_name=subdomain.name).order_by('type', 'name', '-id')
        cache.set(cache_key, dns_records, timeout=3600)
        for dns_record in dns_records:
            cache.set('dns_records:' + str(dns_record.id), dns_record, timeout=dns_record.ttl)
        return dns_records

    @classmethod
    def create_dns_record(cls, provider: BaseDnsRecordProvider | None, subdomain: Subdomain, **kwargs) -> 'Record':
        if not kwargs.get('name', '').endswith(subdomain.name):
            raise DnsRecordBadRequestError('Name is invalid.')
        if kwargs.get('type') in ('NS', 'CNAME', 'MX', 'SRV',) and not kwargs.get('target').endswith('.'):
            kwargs['target'] = kwargs.get('target') + '.'
        dns_record = cls(subdomain_name=subdomain.name, domain=subdomain.domain, **kwargs)
        if provider:
            try:
                provider_dns_record = provider.create_dns_record(subdomain.name, subdomain.domain, **kwargs)
                dns_record.provider_id = provider_dns_record.get('provider_id')
            except DnsRecordProviderError as e:
                logging.error(e)
        dns_record.save()
        cache.delete('dns_records:' + str(subdomain))
        cache.set('dns_records:' + str(dns_record.id), dns_record, timeout=dns_record.ttl)
        return dns_record

    @classmethod
    def retrieve_dns_record(cls, provider: BaseDnsRecordProvider | None, subdomain: Subdomain, id: int) -> 'Record':
        cache_key = 'dns_records:' + str(id)
        cache_value = cache.get(cache_key,
                                next(filter(lambda x: x.id == id, cache.get('records:' + str(subdomain), [])), None))
        if cache_value is not None:
            return cache_value
        try:
            dns_record = cls.objects.get(subdomain_name=subdomain.name, pk=id)
            if provider:
                try:
                    provider_dns_record = provider.retrieve_dns_record(subdomain.name, subdomain.domain,
                                                                       dns_record.provider_id)
                    if provider_dns_record is None:
                        dns_record.delete()
                        dns_record = None
                    else:
                        dns_record.update_by_provider_dns_record(provider_dns_record)
                except DnsRecordProviderError as e:
                    logging.error(e)
            if dns_record is None:
                cache.delete('dns_records:' + str(subdomain))
                cache.delete('dns_records:' + str(id))
            else:
                cache.set(cache_key, dns_record, timeout=dns_record.ttl)
            return dns_record
        except cls.DoesNotExist:
            raise DnsRecordNotFoundError()

    @classmethod
    def update_dns_record(cls, provider: BaseDnsRecordProvider | None, subdomain: Subdomain, id: int,
                          **kwargs) -> 'Record':
        if 'name' in kwargs.keys() and not kwargs.get('name', '').endswith(subdomain.name):
            raise DnsRecordBadRequestError('Name is invalid.')
        if kwargs.get('type') in ('NS', 'CNAME', 'MX', 'SRV',) and not kwargs.get('target').endswith('.'):
            kwargs['target'] = kwargs.get('target') + '.'
        try:
            dns_record = cls.objects.get(subdomain_name=subdomain.name, pk=id)
            for k, v in kwargs.items():
                if k in ['name', 'type', 'service', 'protocol'] and v != getattr(dns_record, k):
                    raise DnsRecordBadRequestError(f'{k.capitalize()} cannot be changed.')
                setattr(dns_record, k, v)
            if provider:
                try:
                    provider.update_dns_record(subdomain.name, subdomain.domain, dns_record.provider_id, **kwargs)
                except DnsRecordProviderError as e:
                    logging.error(e)
            dns_record.save()
            cache.delete('dns_records:' + str(subdomain))
            cache.set('dns_records:' + str(dns_record.id), dns_record, timeout=dns_record.ttl)
            return dns_record
        except cls.DoesNotExist:
            raise DnsRecordNotFoundError()

    @classmethod
    def delete_dns_record(cls, provider: BaseDnsRecordProvider | None, subdomain: Subdomain, id: int) -> None:
        try:
            dns_record = cls.objects.get(subdomain_name=subdomain.name, pk=id)
            if provider:
                try:
                    provider.delete_dns_record(subdomain.name, subdomain.domain, dns_record.provider_id)
                except DnsRecordProviderError as e:
                    logging.error(e)
            dns_record.delete()
            cache.delete('dns_records:' + str(subdomain))
            cache.delete('dns_records:' + str(id))
        except cls.DoesNotExist:
            raise DnsRecordNotFoundError()

    @classmethod
    def export_zone(cls, provider: BaseDnsRecordProvider | None, subdomain: Subdomain) -> str:
        return '\n'.join(map(str, cls.list_dns_records(provider, subdomain)))

    @classmethod
    def import_zone(cls, provider: BaseDnsRecordProvider | None, subdomain: Subdomain, zone: str) -> None:
        lines = list(filter(lambda x: x[0] != ';', map(lambda x: x.strip(), zone.splitlines())))
        for line in lines:
            cls.create_dns_record(provider, subdomain, **cls.parse_dns_record(line))

    @staticmethod
    def split_name(full_name: str) -> tuple[str | None, str | None, str]:
        names = full_name.split('.')
        service = names.pop(0) if len(names) >= 3 and names[0].startswith('_') else None
        protocol = names.pop(0) if len(names) >= 2 and names[0].startswith('_') else None
        name = '.'.join(names)
        return service, protocol, name

    @staticmethod
    def join_name(service: str | None, protocol: str | None, name: str) -> str:
        if service is not None and not service.startswith('_'):
            service = '_' + service
        if protocol is not None and not protocol.startswith('_'):
            protocol = '_' + protocol
        return '.'.join(filter(lambda x: x is not None, [service, protocol, name]))

    @staticmethod
    def split_data(data: str) -> tuple[int | None, int | None, int | None, str]:
        values = data.split()
        priority = int(values[0]) if len(values) > 1 else None
        weight = int(values[1]) if len(values) == 4 else None
        port = int(values[2]) if len(values) == 4 else None
        target = values[-1]
        return priority, weight, port, target

    @staticmethod
    def join_data(priority: int | None, weight: int | None, port: int | None, target: str) -> str:
        return ' '.join(map(str, filter(lambda x: x is not None, [priority, weight, port, target])))

    @classmethod
    def parse_dns_record(cls, raw_record: str) -> dict[str, Any]:
        r = raw_record.split()
        service, protocol, name = cls.split_name(r[0])
        priority, weight, port, target = cls.split_data(r[-1])
        return {
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

    @classmethod
    def synchronize_dns_records(cls, provider: BaseDnsRecordProvider) -> None:
        logging.info('Start synchronizing records.')
        for subdomain in Subdomain.objects.all():
            cls.list_dns_records(provider, subdomain)
        logging.info('End synchronizing records.')

    def update_by_provider_dns_record(self, provider_dns_record: dict[str, Any]) -> bool:
        is_updated = False
        for k, v in provider_dns_record.items():
            if getattr(self, k) != v:
                setattr(self, k, v)
                is_updated = True
        if is_updated:
            self.save()
        return is_updated
