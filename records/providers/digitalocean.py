import os
from typing import Any, Dict, List, Optional

import digitalocean

from domains.models import Domain
from .base import BaseRecordProvider


class DigitalOceanRecordProvider(BaseRecordProvider):
    token = os.environ.get('DIGITALOCEAN_ACCESS_TOKEN')

    def list_records(self, subdomain_name: str, domain: Domain) -> List[Dict[str, Any]]:
        do_domain = digitalocean.Domain(token=self.token, name=domain.name)
        records = do_domain.get_records()
        return list(map(self.record_to_dict, filter(lambda e: e.name.endswith(subdomain_name), records)))

    def create_record(self, subdomain_name: str, domain: Domain, **kwargs) -> Dict[str, Any]:
        if not kwargs.get('name', subdomain_name).endswith(subdomain_name):
            return kwargs
        do_domain = digitalocean.Domain(token=self.token, name=domain.name)
        new_record = do_domain.create_new_domain_record(
            name=kwargs.get('name'),
            ttl=kwargs.get('ttl'),
            type=kwargs.get('ttl'),
            data=kwargs.get('target'),
            priority=kwargs.get('priority'),
            weight=kwargs.get('weight'),
            port=kwargs.get('port'),
        )
        kwargs['provider_id'] = new_record['domain_record']['id']
        return kwargs

    def retrieve_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> Optional[Dict[str, Any]]:
        do_domain = digitalocean.Domain(token=self.token, name=domain.name)
        do_id = int(provider_id)
        records = do_domain.get_records()
        for r in records:
            if r.id == do_id and r.name.endswith(subdomain_name):
                return self.record_to_dict(r)

    def update_record(self, subdomain_name: str, domain: Domain, provider_id: str, **kwargs
                      ) -> Optional[Dict[str, Any]]:
        if not kwargs.get('name', subdomain_name).endswith(subdomain_name):
            return kwargs
        do_domain = digitalocean.Domain(token=self.token, name=subdomain_name)
        do_id = int(provider_id)
        records = do_domain.get_records()
        for r in records:
            if r.id == do_id:
                r.ttl = kwargs.get('ttl')
                r.data = kwargs.get('target')
                if kwargs.get('type') in ['MX', 'SRV']:
                    r.priority = kwargs.get('priority')
                if kwargs.get('type') in ['SRV']:
                    r.weight = kwargs.get('weight')
                    r.port = kwargs.get('port')
                r.save()
        return kwargs

    def delete_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        do_domain = digitalocean.Domain(token=self.token, name=subdomain_name)
        do_id = int(provider_id)
        records = do_domain.get_records()
        for r in records:
            if r.id == do_id and r.name.endswith(subdomain_name):
                r.destroy()

    @staticmethod
    def record_to_dict(record) -> Dict[str, Any]:
        d = {
            'provider_id': record.id,
            'name': record.name,
            'ttl': record.ttl,
            'type': record.type,
            'target': record.data,
        }
        if record.type in ['MX', 'SRV']:
            d.update({'priority': record.priority})
        if record.type in ['SRV']:
            d.update({'weight': record.weight, 'port': record.port})
        return d
