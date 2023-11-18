import os
from typing import Any

import requests

from domains.models import Domain
from .base import BaseDnsRecordProvider
from ..exceptions import DnsRecordProviderError


class VultrDnsRecordProvider(BaseDnsRecordProvider):
    host = 'https://api.vultr.com'
    api_key = os.environ.get('VULTR_API_KEY')
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    def list_dns_records(self, subdomain_name: str, domain: Domain) -> list[dict[str, Any]]:
        response = requests.get(self.host + f'/v2/domains/{domain.name}/records', headers=self.headers,
                                params={
                                    'per_page': 500,
                                })
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return list(filter(lambda x: x.get('name').endswith(subdomain_name),
                           map(self.from_vultr_dns_record, response.json().get('records'))))

    def create_dns_record(self, subdomain_name: str, domain: Domain, **kwargs) -> dict[str, Any]:
        response = requests.post(self.host + f'/v2/domains/{domain.name}/records', headers=self.headers,
                                 json=self.to_vultr_dns_record(kwargs))
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return self.from_vultr_dns_record(response.json().get('record'))

    def retrieve_dns_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> dict[str, Any] | None:
        response = requests.get(self.host + f'/v2/domains/{domain.name}/records/{provider_id}', headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return self.from_vultr_dns_record(response.json().get('record'))

    def update_dns_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs) -> dict[str, Any]:
        response = requests.patch(self.host + f'/v2/domains/{domain.name}/records/{provider_id}', headers=self.headers,
                                  json=self.to_vultr_dns_record(kwargs))
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return kwargs

    def delete_dns_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        response = requests.delete(self.host + f'/v2/domains/{domain.name}/records/{provider_id}', headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())

    def get_nameservers(self, domain: Domain = None) -> list[str]:
        return [
            'ns1.vultr.com',
            'ns2.vultr.com',
        ]

    @staticmethod
    def from_vultr_dns_record(vultr_dns_record: dict[str, Any]) -> dict[str, Any]:
        from ..models import Record
        service, protocol, name = Record.split_name(vultr_dns_record.get('name'))
        _, weight, port, target = Record.split_data('0 ' + vultr_dns_record.get('data'))
        priority = vultr_dns_record.get('priority', -1)
        return {
            'provider_id': str(vultr_dns_record.get('id')),
            'name': name,
            'ttl': vultr_dns_record.get('ttl'),
            'type': vultr_dns_record.get('type'),
            'service': service,
            'protocol': protocol,
            'target': target,
            'priority': priority if priority >= 0 else None,
            'weight': weight,
            'port': port,
        }

    @staticmethod
    def to_vultr_dns_record(dns_record: dict[str, Any]) -> dict[str, Any]:
        from ..models import Record
        name = Record.join_name(dns_record.get('service'), dns_record.get('protocol'), dns_record.get('name'))
        if dns_record.get('type') in ('NS', 'CNAME', 'MX', 'SRV',) and dns_record.get('target').endswith('.'):
            dns_record['target'] = dns_record.get('target')[:-1]
        data = Record.join_data(None, dns_record.get('weight'), dns_record.get('port'), dns_record.get('target'))
        return {
            'name': name,
            'ttl': dns_record.get('ttl'),
            'type': dns_record.get('type'),
            'data': data,
            'priority': dns_record.get('priority'),
        }
