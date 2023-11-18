import os
from typing import Any

import requests
from django.core.cache import cache

from domains.models import Domain
from .base import BaseDnsRecordProvider
from ..exceptions import DnsRecordProviderError


class CloudflareDnsRecordProvider(BaseDnsRecordProvider):
    host = 'https://api.cloudflare.com'
    api_token = os.environ.get('CLOUDFLARE_API_TOKEN')
    headers = {
        'Authorization': f'Bearer {api_token}',
    }

    def list_dns_records(self, subdomain_name: str, domain: Domain) -> list[dict[str, Any]]:
        response = requests.get(self.host + f'/client/v4/zones/{self.get_zone_identifier(domain.name)}/dns_records',
                                headers=self.headers, params={
                                    'per_page': 50000,
                                })
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return list(filter(lambda x: x.get('name').endswith(subdomain_name),
                           map(self.from_cloudflare_dns_record, response.json().get('result'))))

    def create_dns_record(self, subdomain_name: str, domain: Domain, **kwargs) -> dict[str, Any]:
        response = requests.post(self.host + f'/client/v4/zones/{self.get_zone_identifier(domain.name)}/dns_records',
                                 headers=self.headers, json=self.to_cloudflare_dns_record(kwargs))
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return self.from_cloudflare_dns_record(response.json().get('result'))

    def retrieve_dns_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> dict[str, Any] | None:
        response = requests.get(
            self.host + f'/client/v4/zones/{self.get_zone_identifier(domain.name)}/dns_records/{provider_id}',
            headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return self.from_cloudflare_dns_record(response.json().get('result'))

    def update_dns_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs) -> dict[str, Any]:
        response = requests.put(
            self.host + f'/client/v4/zones/{self.get_zone_identifier(domain.name)}/dns_records/{provider_id}',
            headers=self.headers, json=self.to_cloudflare_dns_record(kwargs))
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return self.from_cloudflare_dns_record(response.json().get('result'))

    def delete_dns_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        response = requests.delete(
            self.host + f'/client/v4/zones/{self.get_zone_identifier(domain.name)}/dns_records/{provider_id}',
            headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())

    def get_nameservers(self, domain: Domain = None) -> list[str]:
        response = requests.get(self.host + f'/client/v4/zones/{self.get_zone_identifier(domain.name)}')
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return response.json().get('result', {}).get('name_servers', [])

    def get_zone_identifier(self, domain_name: str) -> str:
        cache_key = 'cloudflare:' + domain_name
        cache_value = cache.get(cache_key)
        if cache_value is not None:
            return cache_value
        response = requests.get(self.host + '/client/v4/zones', headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        zone_identifier = next(map(lambda x: x.get('id'),
                                   filter(lambda x: x.get('name') == domain_name, response.json().get('result', []))))
        cache.set(cache_key, zone_identifier, timeout=86400)
        return zone_identifier

    @staticmethod
    def from_cloudflare_dns_record(cloudflare_dns_record: dict[str, Any]) -> dict[str, Any]:
        from ..models import Record
        service, protocol, name = Record.split_name(cloudflare_dns_record.get('name'))
        _, weight, port, target = Record.split_data(cloudflare_dns_record.get('content'))
        return {
            'provider_id': cloudflare_dns_record.get('id'),
            'name': name,
            'ttl': cloudflare_dns_record.get('ttl'),
            'type': cloudflare_dns_record.get('type'),
            'service': service,
            'protocol': protocol,
            'target': target,
            'priority': cloudflare_dns_record.get('priority'),
            'weight': weight,
            'port': port,
        }

    @staticmethod
    def to_cloudflare_dns_record(dns_record: dict[str, Any]) -> dict[str, Any]:
        from ..models import Record
        content = Record.join_data(dns_record.get('priority'), dns_record.get('weight'), dns_record.get('port'),
                                   dns_record.get('target'))
        name = Record.join_name(dns_record.get('service'), dns_record.get('protocol'), dns_record.get('name'))
        return {
            'content': content,
            'name': name,
            'proxied': False,
            'type': dns_record.get('type'),
            'ttl': dns_record.get('ttl'),
        }
