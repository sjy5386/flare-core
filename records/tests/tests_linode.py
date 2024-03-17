import responses
from django.test import TestCase

from domains.models import Domain
from records.providers import LinodeDnsRecordProvider
from records.providers.mock.linode import MockLinodeDnsRecord


class LinodeDnsRecordProviderTest(TestCase):
    host = 'https://api.linode.com'

    def setUp(self):
        MockLinodeDnsRecord()
        self.provider = LinodeDnsRecordProvider()

    @responses.activate
    def test_get_domain_id(self):
        result = self.provider.get_domain_id('example.org')
        self.assertEqual(1234, result)

    @responses.activate
    def test_list_dns_records(self):
        result = self.provider.list_dns_records('test', Domain(name='example.org'))
        self.assertFalse(any(x['name'] != 'test' for x in result))

    @responses.activate
    def test_create_dns_record(self):
        result = self.provider.create_dns_record('test', Domain(name='example.org'), **{
            'name': 'test',
            'ttl': 604800,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '192.0.2.0',
            'priority': 50,
            'weight': 50,
            'port': 80,
        })
        self.assertDictEqual({
            'provider_id': '123456',
            'name': 'test',
            'ttl': 604800,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '192.0.2.0',
            'priority': 50,
            'weight': 50,
            'port': 80,
        }, result)

    @responses.activate
    def test_retrieve_dns_record(self):
        result = self.provider.retrieve_dns_record('test', Domain(name='example.org'), '123456')
        self.assertDictEqual({
            'provider_id': '123456',
            'name': 'test',
            'ttl': 604800,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '192.0.2.0',
            'priority': 50,
            'weight': 50,
            'port': 80,
        }, result)

    @responses.activate
    def test_update_dns_record(self):
        result = self.provider.update_dns_record('test', Domain(name='example.org'), '123456', **{
            'name': 'test',
            'ttl': 604800,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '192.0.2.0',
            'priority': 50,
            'weight': 50,
            'port': 80,
        })
        self.assertDictEqual({
            'provider_id': '123456',
            'name': 'test',
            'ttl': 604800,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '192.0.2.0',
            'priority': 50,
            'weight': 50,
            'port': 80,
        }, result)

    @responses.activate
    def test_delete_dns_record(self):
        self.provider.delete_dns_record('test', Domain(name='example.org'), '123456')
