import os
from typing import Any, Dict, List, Optional

import digitalocean
from django.core.cache import cache

from domains.models import Domain
from .base import BaseRecordProvider


class DigitalOceanRecordProvider(BaseRecordProvider):
    token = os.environ.get('DIGITALOCEAN_ACCESS_TOKEN')

    def list_records(self, subdomain_name: str, domain: Domain) -> List[Dict[str, Any]]:
        records = self.get_records(domain)
        return list(filter(lambda e: e.get('name').endswith(subdomain_name), records))

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
        cache.delete(domain)
        return kwargs

    def retrieve_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> Optional[Dict[str, Any]]:
        do_id = int(provider_id)
        records = self.get_records(domain)
        try:
            return next(filter(lambda x: int(x.get('provider_id')) == do_id and x.get('name').endswith(subdomain_name),
                               records))
        except StopIteration:
            pass

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
                cache.delete(domain)
                break
        return kwargs

    def delete_record(self, subdomain_name: str, domain: Domain, provider_id: str) -> None:
        do_domain = digitalocean.Domain(token=self.token, name=domain.name)
        do_id = int(provider_id)
        do_records = do_domain.get_records()
        for r in do_records:
            if r.id == do_id and r.name.endswith(subdomain_name):
                r.destroy()
                cache.delete(domain)
                break

    @staticmethod
    def record_to_dict(record) -> Dict[str, Any]:
        from ..models import Record
        service, protocol, name = Record.split_name(record.name)
        d = {
            'provider_id': str(record.id),
            'name': name,
            'ttl': record.ttl,
            'type': record.type,
            'service': service,
            'protocol': protocol,
            'target': record.data,
        }
        if record.type in ['MX', 'SRV']:
            d.update({'priority': record.priority})
        if record.type in ['SRV']:
            d.update({'weight': record.weight, 'port': record.port})
        return d

    def get_records(self, domain: Domain) -> List[Dict[str, Any]]:
        if cache.get(domain) is None:
            do_domain = digitalocean.Domain(token=self.token, name=domain.name)
            do_records = do_domain.get_records()
            cache.set(domain, list(map(self.record_to_dict, do_records)))
        return cache.get(domain)
