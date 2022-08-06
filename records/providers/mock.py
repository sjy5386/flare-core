from typing import Any, Dict, List, Optional

from domains.models import Domain
from .base import BaseRecordProvider


class MockRecordProvider(BaseRecordProvider):
    i = 1
    records = []

    def list_records(self, subdomain_name: str, domain: Domain) -> List[Dict[str, Any]]:
        return list(filter(lambda x: x['subdomain_name'] == subdomain_name, self.records))

    def create_record(self, subdomain_name: str, **kwargs) -> Dict[str, Any]:
        record = {
            'provider_id': str(self.i),
            'subdomain_name': subdomain_name,
        }
        record.update(kwargs)
        self.records.append(record)
        self.i += 1
        return record

    def retrieve_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> Optional[Dict[str, Any]]:
        try:
            return next(filter(lambda x: x['provider_id'] == provider_id, self.records))
        except StopIteration:
            pass

    def update_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs
                      ) -> Optional[Dict[str, Any]]:
        record = self.retrieve_record(subdomain_name, provider_id)
        record.update(kwargs)
        return record

    def delete_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        self.records.remove(self.retrieve_record(subdomain_name, provider_id))
