import os
from typing import Any, Dict, List, Optional

import digitalocean
import requests

from domains.models import Domain
from .base import BaseRecordProvider


class DigitalOceanRecordProvider(BaseRecordProvider):
    host = 'https://api.digitalocean.com'
    token = os.environ.get('DIGITALOCEAN_ACCESS_TOKEN')
    headers = {
        'Authorization': f'Bearer {token}',
    }

    def list_records(self, subdomain_name: str, domain: Domain) -> List[Dict[str, Any]]:
        response = requests.get(self.host + f'/v2/domains/{domain.name}/records', headers=self.headers)
        records = list(filter(lambda x: x.get('name').endswith(subdomain_name),
                              map(self.from_digitalocean_record, response.json().get('domain_records'))))
        return records

    def create_record(self, subdomain_name: str, domain: Domain, **kwargs) -> Dict[str, Any]:
        from ..models import Record
        if not kwargs.get('name', subdomain_name).endswith(subdomain_name):
            return kwargs
        do_domain = digitalocean.Domain(token=self.token, name=domain.name)
        new_record = do_domain.create_new_domain_record(
            name=Record.join_name(kwargs.get('service'), kwargs.get('protocol'), kwargs.get('name')),
            ttl=kwargs.get('ttl'),
            type=kwargs.get('type'),
            data=kwargs.get('target'),
            priority=kwargs.get('priority'),
            weight=kwargs.get('weight'),
            port=kwargs.get('port'),
        )
        kwargs['provider_id'] = str(new_record['domain_record']['id'])
        return kwargs

    def retrieve_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> Optional[Dict[str, Any]]:
        response = requests.get(self.host + f'/v2/domains/{domain.name}/records/{provider_id}', headers=self.headers)
        return self.from_digitalocean_record(response.json().get('domain_record'))

    def update_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs
                      ) -> Optional[Dict[str, Any]]:
        if not kwargs.get('name', subdomain_name).endswith(subdomain_name):
            return kwargs
        do_domain = digitalocean.Domain(token=self.token, name=domain.name)
        do_id = int(provider_id)
        do_records = do_domain.get_records()
        for r in do_records:
            if r.id == do_id:
                r.ttl = kwargs.get('ttl')
                r.data = kwargs.get('target')
                if kwargs.get('type') in ['MX', 'SRV']:
                    r.priority = kwargs.get('priority')
                if kwargs.get('type') in ['SRV']:
                    r.weight = kwargs.get('weight')
                    r.port = kwargs.get('port')
                r.save()
                break
        return kwargs

    def delete_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        do_domain = digitalocean.Domain(token=self.token, name=domain.name)
        do_id = int(provider_id)
        do_records = do_domain.get_records()
        for r in do_records:
            if r.id == do_id and r.name.endswith(subdomain_name):
                r.destroy()
                break

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
