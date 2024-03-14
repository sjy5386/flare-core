import responses
from django.test import TestCase

from domains.models import Domain
from records.providers import VultrDnsRecordProvider
from records.providers.mock.vultr import MockVultrDnsRecord


class VultrDnsRecordProviderTest(TestCase):
    host = 'https://api.vultr.com'

    def setUp(self):
        MockVultrDnsRecord()
        self.provider = VultrDnsRecordProvider()

    @responses.activate
    def test_list_dns_records(self):
        result = self.provider.list_dns_records('www', Domain(name='example.com'))
        self.assertFalse(any(x['name'] != 'www' for x in result))

    @responses.activate
    def test_create_dns_record(self):
        result = self.provider.create_dns_record('www', Domain(name='example.com'), **{
            'name': 'www',
            'ttl': 300,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '192.0.2.123',
            'priority': 0,
            'weight': None,
            'port': None,
        })
        self.assertDictEqual({
            'provider_id': 'cb676a46-66fd-4dfb-b839-443f2e6c0b60',
            'name': 'www',
            'ttl': 300,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '192.0.2.123',
            'priority': 0,
            'weight': None,
            'port': None,
        }, result)

    @responses.activate
    def test_retrieve_dns_record(self):
        result = self.provider.retrieve_dns_record('www', Domain(name='example.com'),
                                                   'cb676a46-66fd-4dfb-b839-443f2e6c0b60')
        self.assertDictEqual({
            'provider_id': 'cb676a46-66fd-4dfb-b839-443f2e6c0b60',
            'name': 'www',
            'ttl': 300,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '192.0.2.123',
            'priority': 0,
            'weight': None,
            'port': None,
        }, result)

    @responses.activate
    def test_update_dns_record(self):
        result = self.provider.update_dns_record('www', Domain(name='example.com'),
                                                 'cb676a46-66fd-4dfb-b839-443f2e6c0b60', **{
                'name': 'www',
                'ttl': 300,
                'type': 'A',
                'service': None,
                'protocol': None,
                'target': '192.0.2.123',
                'priority': 0,
                'weight': None,
                'port': None,
            })
        self.assertDictEqual({
            'provider_id': 'cb676a46-66fd-4dfb-b839-443f2e6c0b60',
            'name': 'www',
            'ttl': 300,
            'type': 'A',
            'service': None,
            'protocol': None,
            'target': '192.0.2.123',
            'priority': 0,
            'weight': None,
            'port': None,
        }, result)

    @responses.activate
    def test_delete_dns_record(self):
        self.provider.delete_dns_record('www', Domain(name='example.com'), 'cb676a46-66fd-4dfb-b839-443f2e6c0b60')
