from typing import Any

import requests

from domains.models import Domain
from .base import BaseDnsRecordProvider
from ..exceptions import RecordProviderError
from ..models import Record


class CloudflareDnsRecordProvider(BaseDnsRecordProvider):
    host = 'https://api.cloudflare.com'

    def list_records(self, subdomain_name: str, domain: Domain) -> list[dict[str, Any]]:
        response = requests.get(self.host + f'/client/v4/zones/{self.get_zone_identifier(domain.name)}/dns_records',
                                params={
                                    'per_page': 50000,
                                })
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise RecordProviderError(response.json())
        return list(filter(lambda x: x.get('name').endswith(subdomain_name),
                           map(self.from_cloudflare_record, response.json().get('result'))))

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

    def get_zone_identifier(self, domain_name: str) -> str:
        response = requests.get(self.host + '/client/v4/zones')
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise RecordProviderError(response.json())
        zone_identifier = next(map(lambda x: x.get('id'),
                                   filter(lambda x: x.get('name') == domain_name, response.json().get('result', []))))
        return zone_identifier

    @staticmethod
    def from_cloudflare_record(cloudflare_record: dict[str, Any]) -> dict[str, Any]:
        service, protocol, name = Record.split_name(cloudflare_record.get('name'))
        priority, weight, port, target = Record.split_data(cloudflare_record.get('content'))
        return {
            'provider_id': cloudflare_record.get('id'),
            'name': name,
            'ttl': cloudflare_record.get('ttl'),
            'type': cloudflare_record.get('type'),
            'service': service,
            'protocol': protocol,
            'target': target,
            'priority': priority,
            'weight': weight,
            'port': port,
        }
