import os
from typing import Any

import requests
from django.core.cache import cache

from domains.models import Domain
from .base import BaseDnsRecordProvider
from ..exceptions import DnsRecordProviderError


class LinodeDnsRecordProvider(BaseDnsRecordProvider):
    host = 'https://api.linode.com'
    token = os.environ.get('LINODE_ACCESS_TOKEN')
    headers = {
        'Authorization': f'Bearer {token}',
    }

    def list_dns_records(self, subdomain_name: str, domain: Domain) -> list[dict[str, Any]]:
        response = requests.get(self.host + f'/v4/domains/{self.get_domain_id(domain.name)}/records',
                                headers=self.headers, params={
                'page_size': 500,
            })
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return list(filter(lambda x: x.get('name').endswith(subdomain_name),
                           map(self.from_linode_dns_record, response.json().get('data'))))

    def create_dns_record(self, subdomain_name: str, domain: Domain, **kwargs) -> dict[str, Any]:
        response = requests.post(self.host + f'/v4/domains/{self.get_domain_id(domain.name)}/records',
                                 headers=self.headers, json=self.to_linode_dns_record(kwargs))
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return self.from_linode_dns_record(response.json())

    def retrieve_dns_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> dict[str, Any] | None:
        response = requests.get(self.host + f'/v4/domains/{self.get_domain_id(domain.name)}/records/{provider_id}',
                                headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return self.from_linode_dns_record(response.json())

    def update_dns_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs) -> dict[str, Any]:
        response = requests.put(self.host + f'/v4/domains/{self.get_domain_id(domain.name)}/records/{provider_id}',
                                headers=self.headers, json=self.to_linode_dns_record(kwargs))
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        return self.from_linode_dns_record(response.json())

    def delete_dns_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        response = requests.delete(self.host + f'/v4/domains/{self.get_domain_id(domain.name)}/records/{provider_id}',
                                   headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())

    def get_nameservers(self, domain: Domain = None) -> list[str]:
        return [
            'ns1.linode.com',
            'ns2.linode.com',
            'ns3.linode.com',
            'ns4.linode.com',
            'ns5.linode.com',
        ]

    def get_domain_id(self, domain_name: str) -> int:
        cache_key = 'linode:' + domain_name
        cache_value = cache.get(cache_key)
        if cache_value is not None:
            return cache_value
        response = requests.get(self.host + '/v4/domains', headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise DnsRecordProviderError(response.json())
        domain_id = next(map(lambda x: x.get('id'),
                             filter(lambda x: x.get('domain') == domain_name, response.json().get('data', []))))
        cache.set(cache_key, domain_id, timeout=86400)
        return domain_id

    @staticmethod
    def from_linode_dns_record(linode_dns_record: dict[str, Any]) -> dict[str, Any]:
        return {
            'provider_id': str(linode_dns_record.get('id')),
            'name': linode_dns_record.get('name'),
            'ttl': linode_dns_record.get('ttl_sec'),
            'type': linode_dns_record.get('type'),
            'service': linode_dns_record.get('service'),
            'protocol': linode_dns_record.get('protocol'),
            'target': linode_dns_record.get('target'),
            'priority': linode_dns_record.get('priority'),
            'weight': linode_dns_record.get('weight'),
            'port': linode_dns_record.get('port'),
        }

    @staticmethod
    def to_linode_dns_record(dns_record: dict[str, Any]) -> dict[str, Any]:
        return {
            'name': dns_record.get('name'),
            'ttl_sec': dns_record.get('ttl'),
            'type': dns_record.get('type'),
            'service': dns_record.get('service'),
            'protocol': dns_record.get('protocol'),
            'target': dns_record.get('target'),
            'priority': dns_record.get('priority'),
            'weight': dns_record.get('weight'),
            'port': dns_record.get('port'),
        }
