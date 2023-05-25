import os
from typing import Optional, Dict, Any, List

import requests
from django.core.cache import cache

from domains.models import Domain
from .base import BaseRecordProvider


class LinodeRecordProvider(BaseRecordProvider):
    host = 'https://api.linode.com'
    token = os.environ.get('LINODE_ACCESS_TOKEN')
    headers = {
        'Authorization': f'Bearer {token}',
    }

    def list_records(self, subdomain_name: str, domain: Domain) -> List[Dict[str, Any]]:
        response = requests.get(self.host + f'/v4/domains/{self.get_domain_id(domain.name)}/records',
                                headers=self.headers)
        response.raise_for_status()
        return list(filter(lambda x: x.get('name').endswith(subdomain_name),
                           map(self.from_linode_record, response.json().get('data'))))

    def create_record(self, subdomain_name: str, domain: Domain, **kwargs) -> Dict[str, Any]:
        response = requests.post(self.host + f'/v4/domains/{self.get_domain_id(domain.name)}/records',
                                 headers=self.headers, json=self.to_linode_record(kwargs))
        response.raise_for_status()
        return self.from_linode_record(response.json())

    def retrieve_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> Optional[Dict[str, Any]]:
        response = requests.get(self.host + f'/v4/domains/{self.get_domain_id(domain.name)}/records/{provider_id}',
                                headers=self.headers)
        response.raise_for_status()
        return self.from_linode_record(response.json())

    def update_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs
                      ) -> Optional[Dict[str, Any]]:
        response = requests.put(self.host + f'/v4/domains/{self.get_domain_id(domain.name)}/records/{provider_id}',
                                headers=self.headers, json=self.to_linode_record(kwargs))
        response.raise_for_status()
        return self.from_linode_record(response.json())

    def delete_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        response = requests.delete(self.host + f'/v4/domains/{self.get_domain_id(domain.name)}/records/{provider_id}',
                                   headers=self.headers)
        response.raise_for_status()

    def get_nameservers(self, domain: Domain) -> List[str]:
        pass

    def get_domain_id(self, domain_name: str) -> int:
        cache_key = 'linode:' + domain_name
        cache_value = cache.get(cache_key)
        if cache_value is not None:
            return cache_value
        response = requests.get(self.host + '/domains', headers=self.headers)
        response.raise_for_status()
        domain_id = next(map(lambda x: x.get('id'),
                             filter(lambda x: x.get('domain') == domain_name, response.json().get('data', []))))
        cache.set(cache_key, domain_id, timeout=86400)
        return domain_id

    @staticmethod
    def from_linode_record(linode_record: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'provider_id': str(linode_record.get('id')),
            'name': linode_record.get('name'),
            'ttl': linode_record.get('ttl_sec'),
            'type': linode_record.get('type'),
            'service': linode_record.get('service'),
            'protocol': linode_record.get('protocol'),
            'target': linode_record.get('target'),
            'priority': linode_record.get('priority'),
            'weight': linode_record.get('weight'),
            'port': linode_record.get('port'),
        }

    @staticmethod
    def to_linode_record(record: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'name': record.get('name'),
            'ttl_sec': record.get('ttl'),
            'type': record.get('type'),
            'service': record.get('service'),
            'protocol': record.get('protocol'),
            'target': record.get('target'),
            'priority': record.get('priority'),
            'weight': record.get('weight'),
            'port': record.get('port'),
        }
