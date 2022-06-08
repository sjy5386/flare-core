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
        record.id = self.i
        self.i += 1
        self.records.append(record)
        return record

    def retrieve_record(self, subdomain: Subdomain, id) -> Record:
        for r in self.records:
            if r.id == id:
                return r

    def update_record(self, subdomain: Subdomain, id, record: Record) -> Record:
        if not record.name.endswith(subdomain.name):
            return record
        for r in self.records:
            if r.id == id:
                r = record
                r.id = id
                return r

    def delete_record(self, subdomain: Subdomain, id):
        for r in self.records:
            if r.id == id and r.name.endswith(subdomain.name):
                self.records.remove(r)
                return
