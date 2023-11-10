from typing import Any

from domains.models import Domain
from .base import BaseDnsRecordProvider


class CloudflareDnsRecordProvider(BaseDnsRecordProvider):
    host = 'https://api.cloudflare.com'

    def list_records(self, subdomain_name: str, domain: Domain) -> list[dict[str, Any]]:
        pass

    def create_record(self, subdomain_name: str, domain: Domain, **kwargs) -> dict[str, Any]:
        pass

    def retrieve_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> dict[str, Any] | None:
        pass

    def update_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs) -> dict[str, Any]:
        pass

    def delete_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        pass

    def get_nameservers(self, domain: Domain = None) -> list[str]:
        pass
