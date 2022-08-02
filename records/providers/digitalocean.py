import os
from typing import List

import digitalocean

from subdomains.models import Subdomain
from .base import BaseRecordProvider
from ..types import Record


class DigitalOceanRecordProvider(BaseRecordProvider):
    token = os.environ.get('DIGITALOCEAN_ACCESS_TOKEN')

    def list_records(self, subdomain: Subdomain) -> List[Record]:
        domain = digitalocean.Domain(token=self.token, name=subdomain.domain.name)
        records = domain.get_records()
        return list(map(self.provider_record_object_to_record_object,
                        filter(lambda e: e.name.endswith(subdomain.name), records)))

    def create_record(self, subdomain: Subdomain, record: Record) -> Record:
        if not record.name.endswith(subdomain.name):
            return record
        domain = digitalocean.Domain(token=self.token, name=subdomain.domain.name)
        new_record = domain.create_new_domain_record(
            name=record.name,
            ttl=record.ttl,
            type=record.type,
            data=record.target,
            priority=record.priority,
            weight=record.priority,
            port=record.port,
        )
        record.id = new_record['domain_record']['id']
        return record

    def retrieve_record(self, subdomain: Subdomain, id) -> Record:
        domain = digitalocean.Domain(token=self.token, name=subdomain.domain.name)
        id = int(id)
        records = domain.get_records()
        for r in records:
            if r.id == id and r.name.endswith(subdomain.name):
                return self.provider_record_object_to_record_object(r)

    def update_record(self, subdomain: Subdomain, id, record: Record) -> Record:
        if not record.name.endswith(subdomain.name):
            return record
        domain = digitalocean.Domain(token=self.token, name=subdomain.domain.name)
        id = int(id)
        records = domain.get_records()
        for r in records:
            if r.id == id:
                r.name = record.name
                r.ttl = record.ttl
                r.type = record.type
                r.data = record.target
                if record.type == 'MX' or record.type == 'SRV':
                    r.priority = record.priority
                if record.type == 'SRV':
                    r.weight = record.weight
                    r.port = record.port
                r.save()
        return record

    def delete_record(self, subdomain: Subdomain, id):
        domain = digitalocean.Domain(token=self.token, name=subdomain.domain.name)
        id = int(id)
        records = domain.get_records()
        for r in records:
            if r.id == id and r.name.endswith(subdomain.name):
                r.destroy()

    def provider_record_object_to_record_object(self, provider_record_object) -> Record:
        kwargs = {
            'identifier': provider_record_object.id
        }
        if provider_record_object.type == 'MX' or provider_record_object == 'SRV':
            kwargs['priority'] = provider_record_object.priority
        if provider_record_object.type == 'SRV':
            kwargs['weight'] = provider_record_object.weight
            kwargs['port'] = provider_record_object.port
        record = Record(provider_record_object.name, provider_record_object.ttl, provider_record_object.type,
                        provider_record_object.data, **kwargs)
        return record
