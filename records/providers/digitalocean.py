import os
from typing import Any, Dict, List, Optional

import requests
from requests import HTTPError

from domains.models import Domain
from .base import BaseRecordProvider
from ..exceptions import RecordProviderError


class DigitalOceanRecordProvider(BaseRecordProvider):
    host = 'https://api.digitalocean.com'
    token = os.environ.get('DIGITALOCEAN_ACCESS_TOKEN')
    headers = {
        'Authorization': f'Bearer {token}',
    }

    def list_records(self, subdomain_name: str, domain: Domain) -> List[Dict[str, Any]]:
        response = requests.get(self.host + f'/v2/domains/{domain.name}/records', headers=self.headers)
        try:
            response.raise_for_status()
        except HTTPError:
            raise RecordProviderError(response.json())
        return list(filter(lambda x: x.get('name').endswith(subdomain_name),
                           map(self.from_digitalocean_record, response.json().get('domain_records'))))

    def create_record(self, subdomain_name: str, domain: Domain, **kwargs) -> Dict[str, Any]:
        response = requests.post(self.host + f'/v2/domains/{domain.name}/records', headers=self.headers,
                                 json=self.to_digitalocean_record(kwargs))
        try:
            response.raise_for_status()
        except HTTPError:
            raise RecordProviderError(response.json())
        return self.from_digitalocean_record(response.json().get('domain_record'))

    def retrieve_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> Optional[Dict[str, Any]]:
        response = requests.get(self.host + f'/v2/domains/{domain.name}/records/{provider_id}', headers=self.headers)
        try:
            response.raise_for_status()
        except HTTPError:
            raise RecordProviderError(response.json())
        return self.from_digitalocean_record(response.json().get('domain_record'))

    def update_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs) -> Dict[str, Any]:
        response = requests.put(self.host + f'/v2/domains/{domain.name}/records/{provider_id}', headers=self.headers,
                                json=self.to_digitalocean_record(kwargs))
        try:
            response.raise_for_status()
        except HTTPError:
            raise RecordProviderError(response.json())
        return self.from_digitalocean_record(response.json().get('domain_record'))

    def delete_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        response = requests.delete(self.host + f'/v2/domains/{domain.name}/records/{provider_id}', headers=self.headers)
        try:
            response.raise_for_status()
        except HTTPError:
            raise RecordProviderError(response.json())

    def get_nameservers(self, domain: Domain = None) -> List[str]:
        return [
            'ns1.digitalocean.com',
            'ns2.digitalocean.com',
            'ns3.digitalocean.com',
        ]

    @staticmethod
    def from_digitalocean_record(digitalocean_record: Dict[str, Any]) -> Dict[str, Any]:
        from ..models import Record
        service, protocol, name = Record.split_name(digitalocean_record.get('name'))
        return {
            'provider_id': str(digitalocean_record.get('id')),
            'name': name,
            'ttl': digitalocean_record.get('ttl'),
            'type': digitalocean_record.get('type'),
            'service': service,
            'protocol': protocol,
            'target': digitalocean_record.get('data'),
            'priority': digitalocean_record.get('priority'),
            'weight': digitalocean_record.get('weight'),
            'port': digitalocean_record.get('port'),
        }

    @staticmethod
    def to_digitalocean_record(record: Dict[str, Any]) -> Dict[str, Any]:
        from ..models import Record
        name = Record.join_name(record.get('service'), record.get('protocol'), record.get('name'))
        return {
            'name': name,
            'ttl': record.get('ttl'),
            'type': record.get('type'),
            'data': record.get('target'),
            'priority': record.get('priority'),
            'weight': record.get('weight'),
            'port': record.get('port'),
        }
