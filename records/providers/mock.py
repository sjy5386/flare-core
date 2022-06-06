from typing import List

from subdomains.models import Subdomain
from .base import BaseProvider
from ..types import Record


class MockProvider(BaseProvider):
    i = 1
    records = []

    def list_records(self, subdomain: Subdomain) -> List[Record]:
        return self.records

    def create_record(self, subdomain: Subdomain, record: Record) -> Record:
        record.identifier = self.i
        self.i += 1
        self.records.append(record)
        return record

    def retrieve_record(self, subdomain: Subdomain, identifier) -> Record:
        for r in self.records:
            if r.identifier == identifier:
                return r

    def update_record(self, subdomain: Subdomain, identifier, record: Record) -> Record:
        if not record.name.endswith(subdomain.name):
            return record
        for r in self.records:
            if r.identifier == identifier:
                r = record
                r.identifier = identifier
                return r

    def delete_record(self, subdomain: Subdomain, identifier):
        for r in self.records:
            if r.identifier == identifier and r.name.endswith(subdomain.name):
                self.records.remove(r)
                return
