import os
from typing import List

import digitalocean

from subdomains.models import Subdomain
from .types import Record


class BaseProvider:
    def list_records(self, subdomain: Subdomain) -> List[Record]:
        pass

    def create_record(self, subdomain: Subdomain, record: Record) -> Record:
        pass

    def retrieve_record(self, subdomain: Subdomain, identifier) -> Record:
        pass

    def update_record(self, subdomain: Subdomain, identifier, record: Record) -> Record:
        pass

    def delete_record(self, subdomain: Subdomain, identifier):
        pass

    def export_zone(self, subdomain: Subdomain) -> str:
        records = self.list_records(subdomain)
        zone = ''
        for record in records:
            zone += str(record) + '\n'
        return zone

    def import_zone(self, subdomain: Subdomain, zone: str):
        lines = zone.splitlines()
        for line in lines:
            if line[0] == ';':
                continue
            r = line.split()
            record = Record(name=r[0], ttl=int(r[1]), r_type=r[3], data=' '.join(r[4:]))
            self.create_record(subdomain, record)

    def provider_record_object_to_record_object(self, provider_record_object) -> Record:
        pass

    def record_object_to_provider_record_object(self, record_object: Record):
        pass


class DigitalOceanProvider(BaseProvider):
    token = os.environ.get('DIGITALOCEAN_TOKEN')

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
            type=record.r_type,
            data=record.data
        )
        record.identifier = new_record.id
        return record

    def retrieve_record(self, subdomain: Subdomain, identifier) -> Record:
        domain = digitalocean.Domain(token=self.token, name=subdomain.domain.name)
        identifier = int(identifier)
        records = domain.get_records()
        for r in records:
            if r.id == identifier and r.name.endswith(subdomain.name):
                return self.provider_record_object_to_record_object(r)

    def update_record(self, subdomain: Subdomain, identifier, record: Record) -> Record:
        if not record.name.endswith(subdomain.name):
            return record
        domain = digitalocean.Domain(token=self.token, name=subdomain.domain.name)
        identifier = int(identifier)
        records = domain.get_records()
        for r in records:
            if r.id == identifier:
                r.name = record.name
                r.ttl = record.ttl
                r.type = record.r_type
                r.data = record.data
        return record

    def delete_record(self, subdomain: Subdomain, identifier):
        domain = digitalocean.Domain(token=self.token, name=subdomain.domain.name)
        identifier = int(identifier)
        records = domain.get_records()
        for r in records:
            if r.id == identifier and r.name.endswith(subdomain.name):
                r.destroy()

    def provider_record_object_to_record_object(self, provider_record_object) -> Record:
        record = Record(provider_record_object.name, provider_record_object.ttl, provider_record_object.type,
                        provider_record_object.data)
        record.identifier = provider_record_object.id
        return record


PROVIDER_CLASS = DigitalOceanProvider
