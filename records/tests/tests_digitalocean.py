import responses
from django.test import TestCase

from domains.models import Domain
from records.providers import DigitalOceanDnsRecordProvider
from records.providers.mock.digitalocean import MockDigitalOceanDnsRecord


class DigitalOceanDnsRecordProviderTest(TestCase):
    host = 'https://api.linode.com'

    def setUp(self):
        MockDigitalOceanDnsRecord()
        self.provider = DigitalOceanDnsRecordProvider()

    @responses.activate
    def test_list_dns_records(self):
        result = self.provider.list_dns_records('test', Domain(name='example.com'))
        self.assertFalse(any(x['name'] != 'test' for x in result))

    @responses.activate
    def test_create_dns_record(self):
        result = self.provider.create_dns_record('www', Domain(name='example.com'), **{
            'name': 'www',
            'ttl': 1800,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '162.10.66.0',
            'priority': None,
            'weight': None,
            'port': None,
        })
        self.assertDictEqual({
            'provider_id': '28448433',
            'name': 'www',
            'ttl': 1800,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '162.10.66.0',
            'priority': None,
            'weight': None,
            'port': None,
        }, result)

    @responses.activate
    def test_retrieve_dns_record(self):
        result = self.provider.retrieve_dns_record('blog', Domain(name='example.com'), '3352896')
        self.assertDictEqual({
            'provider_id': '3352896',
            'name': 'blog',
            'ttl': 1800,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '162.10.66.0',
            'priority': None,
            'weight': None,
            'port': None,
        }, result)

    @responses.activate
    def test_update_dns_record(self):
        result = self.provider.update_dns_record('blog', Domain(name='example.com'), '3352896', **{
            'name': 'blog',
            'ttl': 1800,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '162.10.66.0',
            'priority': None,
            'weight': None,
            'port': None,
        })
        self.assertDictEqual({
            'provider_id': '3352896',
            'name': 'blog',
            'ttl': 1800,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '162.10.66.0',
            'priority': None,
            'weight': None,
            'port': None,
        }, result)

    @responses.activate
    def test_delete_dns_record(self):
        self.provider.delete_dns_record('blog', Domain(name='example.com'), '3352896')
