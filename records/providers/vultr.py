import os
from typing import Any

import requests

from domains.models import Domain
from .base import BaseRecordProvider
from ..exceptions import RecordProviderError


class VultrRecordProvider(BaseRecordProvider):
    host = 'https://api.vultr.com'
    api_key = os.environ.get('VULTR_API_KEY')
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    def list_records(self, subdomain_name: str, domain: Domain) -> list[dict[str, Any]]:
        response = requests.get(self.host + f'/v2/domains/{domain.name}/records', headers=self.headers,
                                params={
                                    'per_page': 500,
                                })
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise RecordProviderError(response.json())
        return list(filter(lambda x: x.get('name').endswith(subdomain_name + '.' + domain.name),
                           map(self.from_vultr_record, response.json().get('records'))))

    def create_record(self, subdomain_name: str, domain: Domain, **kwargs) -> dict[str, Any]:
        response = requests.post(self.host + f'/v2/domains/{domain.name}/records', headers=self.headers,
                                 json=self.to_vultr_record(kwargs))
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise RecordProviderError(response.json())
        return self.from_vultr_record(response.json().get('record'))

    def retrieve_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> dict[str, Any] | None:
        response = requests.get(self.host + f'/v2/domains/{domain.name}/records/{provider_id}', headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise RecordProviderError(response.json())
        return self.from_vultr_record(response.json().get('record'))

    def update_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs) -> dict[str, Any]:
        response = requests.patch(self.host + f'/v2/domains/{domain.name}/records/{provider_id}', headers=self.headers,
                                  json=self.to_vultr_record(kwargs))
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise RecordProviderError(response.json())
        return kwargs

    def delete_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        response = requests.delete(self.host + f'/v2/domains/{domain.name}/records/{provider_id}', headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise RecordProviderError(response.json())

    def get_nameservers(self, domain: Domain = None) -> list[str]:
        return [
            'ns1.vultr.com',
            'ns2.vultr.com',
        ]

    @staticmethod
    def from_vultr_record(vultr_record: dict[str, Any]) -> dict[str, Any]:
        from ..models import Record
        service, protocol, name = Record.split_name(vultr_record.get('name'))
        priority, weight, port, target = Record.split_data('0 ' + vultr_record.get('data'))
        return {
            'provider_id': str(vultr_record.get('id')),
            'name': name,
            'ttl': vultr_record.get('ttl'),
            'type': vultr_record.get('type'),
            'service': service,
            'protocol': protocol,
            'target': target,
            'priority': vultr_record.get('priority'),
            'weight': weight,
            'port': port,
        }

    @staticmethod
    def to_vultr_record(record: dict[str, Any]) -> dict[str, Any]:
        from ..models import Record
        name = Record.join_name(record.get('service'), record.get('protocol'), record.get('name'))
        data = Record.join_data(None, record.get('weight'), record.get('port'), record.get('target'))
        return {
            'name': name,
            'ttl': record.get('ttl'),
            'type': record.get('type'),
            'data': data,
            'priority': record.get('priority'),
        }
