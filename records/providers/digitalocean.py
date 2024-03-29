import os
from typing import Any

import requests

from domains.models import Domain
from .base import BaseDnsRecordProvider
from ..exceptions import DnsRecordProviderError


class DigitalOceanDnsRecordProvider(BaseDnsRecordProvider):
    host = 'https://api.digitalocean.com'
    token = os.environ.get('DIGITALOCEAN_ACCESS_TOKEN')
    headers = {
        'Authorization': f'Bearer {token}',
    }

    def list_dns_records(self, subdomain_name: str, domain: Domain) -> list[dict[str, Any]]:
        response = requests.get(self.host + f'/v2/domains/{domain.name}/records', headers=self.headers,
                                params={
                                    'per_page': 200,
                                })
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return list(filter(lambda x: x.get('name').endswith(subdomain_name),
                           map(self.from_digitalocean_dns_record, response.json().get('domain_records'))))

    def create_dns_record(self, subdomain_name: str, domain: Domain, **kwargs) -> dict[str, Any]:
        response = requests.post(self.host + f'/v2/domains/{domain.name}/records', headers=self.headers,
                                 json=self.to_digitalocean_dns_record(kwargs))
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return self.from_digitalocean_dns_record(response.json().get('domain_record'))

    def retrieve_dns_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> dict[str, Any] | None:
        response = requests.get(self.host + f'/v2/domains/{domain.name}/records/{provider_id}', headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return self.from_digitalocean_dns_record(response.json().get('domain_record'))

    def update_dns_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs) -> dict[str, Any]:
        response = requests.put(self.host + f'/v2/domains/{domain.name}/records/{provider_id}', headers=self.headers,
                                json=self.to_digitalocean_dns_record(kwargs))
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return self.from_digitalocean_dns_record(response.json().get('domain_record'))

    def delete_dns_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        response = requests.delete(self.host + f'/v2/domains/{domain.name}/records/{provider_id}', headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())

    def get_nameservers(self, domain: Domain = None) -> list[str]:
        return [
            'ns1.digitalocean.com',
            'ns2.digitalocean.com',
            'ns3.digitalocean.com',
        ]

    @staticmethod
    def from_digitalocean_dns_record(digitalocean_dns_record: dict[str, Any]) -> dict[str, Any]:
        from ..models import Record
        service, protocol, name = Record.split_name(digitalocean_dns_record.get('name'))
        return {
            'provider_id': str(digitalocean_dns_record.get('id')),
            'name': name,
            'ttl': digitalocean_dns_record.get('ttl'),
            'type': digitalocean_dns_record.get('type'),
            'service': service,
            'protocol': protocol,
            'target': digitalocean_dns_record.get('data'),
            'priority': digitalocean_dns_record.get('priority'),
            'weight': digitalocean_dns_record.get('weight'),
            'port': digitalocean_dns_record.get('port'),
        }

    @staticmethod
    def to_digitalocean_dns_record(dns_record: dict[str, Any]) -> dict[str, Any]:
        from ..models import Record
        name = Record.join_name(dns_record.get('service'), dns_record.get('protocol'), dns_record.get('name'))
        return {
            'name': name,
            'ttl': dns_record.get('ttl'),
            'type': dns_record.get('type'),
            'data': dns_record.get('target'),
            'priority': dns_record.get('priority'),
            'weight': dns_record.get('weight'),
            'port': dns_record.get('port'),
        }
