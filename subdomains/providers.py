from typing import List

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
