from typing import List

import digitalocean

from .models import Subdomain
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
            record = Record(name=r[0], ttl=int(r[1]), record_type=r[3], data=' '.join(r[4:]))
            self.create_record(subdomain, record)


class DigitalOceanProvider(BaseProvider):
    token = ''

    def list_records(self, subdomain: Subdomain) -> List[Record]:
        domain = digitalocean.Domain(token=self.token, name=subdomain.domain.name)
        records = domain.get_records()
        return list(map(lambda e: Record(name=e.name, ttl=e.ttl, record_type=e.type, data=e.data),
                        filter(lambda e: e.name.endswith(subdomain.name), records)))

    def create_record(self, subdomain: Subdomain, record: Record) -> Record:
        if not record.name.endswith(subdomain.name):
            return record
        domain = digitalocean.Domain(token=self.token, name=subdomain.domain.name)
        new_record = domain.create_new_domain_record(
            name=record.name,
            ttl=record.ttl,
            type=record.record_type,
            data=record.data
        )
        record.id = new_record.id
        return record

    def retrieve_record(self, subdomain: Subdomain, identifier) -> Record:
        domain = digitalocean.Domain(token=self.token, name=subdomain.domain.name)
        records = domain.get_records()
        for r in records:
            if r.id == identifier:
                return Record(name=r.name, ttl=r.ttl, record_type=r.type, data=r.data)

    def update_record(self, subdomain: Subdomain, identifier, record: Record) -> Record:
        if not record.name.endswith(subdomain.name):
            return record
        domain = digitalocean.Domain(token=self.token, name=subdomain.domain.name)
        records = domain.get_records()
        for r in records:
            if r.id == identifier:
                r.name = record.name
                r.ttl = record.ttl
                r.type = record.record_type
                r.data = record.data
        return record

    def delete_record(self, subdomain: Subdomain, identifier):
        domain = digitalocean.Domain(token=self.token, name=subdomain.domain.name)
        records = domain.get_records()
        for r in records:
            if r.id == identifier:
                r.destroy()
