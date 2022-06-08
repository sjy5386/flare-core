from typing import List

from subdomains.models import Subdomain
from ..types import Record


class BaseProvider:
    def list_records(self, subdomain: Subdomain) -> List[Record]:
        pass

    def create_record(self, subdomain: Subdomain, record: Record) -> Record:
        pass

    def retrieve_record(self, subdomain: Subdomain, id) -> Record:
        pass

    def update_record(self, subdomain: Subdomain, id, record: Record) -> Record:
        pass

    def delete_record(self, subdomain: Subdomain, id):
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
            record = Record(r[0], int(r[1]), r[3], ' '.join(r[4:]))
            self.create_record(subdomain, record)

    def provider_record_object_to_record_object(self, provider_record_object) -> Record:
        pass

    def record_object_to_provider_record_object(self, record_object: Record):
        pass
