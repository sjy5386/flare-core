import uuid
from typing import Any, Dict, List, Optional

from domains.models import Domain
from .base import BaseRecordProvider


class MockRecordProvider(BaseRecordProvider):
    records = []

    def list_records(self, subdomain_name: str, domain: Domain) -> List[Dict[str, Any]]:
        return list(filter(lambda x: x['subdomain_name'] == subdomain_name and x['domain'] == domain, self.records))

    def create_record(self, subdomain_name: str, domain: Domain, **kwargs) -> Dict[str, Any]:
        record = {
            'provider_id': str(uuid.uuid4()),
            'subdomain_name': subdomain_name,
            'domain': domain,
        }
        record.update(kwargs)
        self.records.append(record)
        return record

    def retrieve_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> Optional[Dict[str, Any]]:
        try:
            return next(filter(lambda x: x['provider_id'] == provider_id, self.records))
        except StopIteration:
            pass

    def update_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs
                      ) -> Optional[Dict[str, Any]]:
        record = self.retrieve_record(subdomain_name, domain, provider_id)
        record.update(kwargs)
        return record

    def delete_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        record = self.retrieve_record(subdomain_name, domain, provider_id)
        if record in self.records:
            self.records.remove(record)

    def get_nameservers(self, domain: Domain) -> List[str]:
        pass

    def get_records(self, domain: Domain) -> List[Dict[str, Any]]:
        return list(filter(lambda x: x['domain'] == domain, self.records))
