import datetime

from django.test import TestCase

from accounts.tests import get_mock_users
from contacts.tests import get_mock_contacts
from domains.tests import get_mock_domains
from subdomains.tests import get_mock_subdomains
from .models import Record


def get_mock_records(count: int = 1, **kwargs) -> list[Record]:
    return [Record.objects.create(**kwargs) for _ in range(count)]


class RecordTest(TestCase):
    def setUp(self) -> None:
        self.user = get_mock_users(
            username='alice', password='test', email='alice@example.com',
            first_name='Alice', last_name='Test',
        )[0]
        self.domain = get_mock_domains(
            name='example.com',
            user=self.user,
        )[0]
        self.contact = get_mock_contacts(
            user=self.user,
            name='test',
            street='test',
            city='test',
            state_province='test',
            postal_code='0',
            country='US',
            phone='+1.1234567890',
            email='test@example.com',
        )[0]
        self.subdomain = get_mock_subdomains(
            user=self.user,
            name='test',
            domain=self.domain,
            expiry=datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=90),
            registrant=self.contact,
            admin=self.contact,
            tech=self.contact,
            billing=self.contact,
        )[0]
        self.record = get_mock_records(
            subdomain_name='test',
            domain=self.domain,
            name='test',
            type='A',
            target='127.0.0.1',
        )[0]

    def test_list_records(self):
        result = Record.list_records(None, self.subdomain)
        self.assertIn(self.record, result)

    def test_create_record(self):
        kwargs = {
            'name': 'test',
            'ttl': 3600,
            'type': 'AAAA',
            'service': None,
            'protocol': None,
            'priority': None,
            'weight': None,
            'port': None,
            'target': '::1',
        }
        result = Record.create_record(None, self.subdomain, **kwargs)
        for k, v in kwargs.items():
            self.assertEqual(getattr(result, k), v)

    def test_retrieve_record(self):
        result = Record.retrieve_record(None, self.subdomain, self.record.id)
        self.assertEqual(result, self.record)

    def test_update_record(self):
        kwargs = {
            'ttl': 300,
            'target': '1.1.1.1',
        }
        result = Record.update_record(None, self.subdomain, self.record.id, **kwargs)
        for k, v in kwargs.items():
            self.assertEqual(getattr(result, k), v)

    def test_delete_record(self):
        Record.delete_record(None, self.subdomain, self.record.id)

    def test_split_name(self):
        result = Record.split_name('example.com')
        self.assertEqual(result, (None, None, 'example.com'))
        result = Record.split_name('_sip._tcp.example.com')
        self.assertEqual(result, ('_sip', '_tcp', 'example.com'))

    def test_join_name(self):
        result = Record.join_name(None, None, 'example.com')
        self.assertEqual(result, 'example.com')
        result = Record.join_name('_sip', '_tcp', 'example.com')
        self.assertEqual(result, '_sip._tcp.example.com')

    def test_split_data(self):
        result = Record.split_data('example.com')
        self.assertEqual(result, (None, None, None, 'example.com'))
        result = Record.split_data('10 example.com')
        self.assertEqual(result, (10, None, None, 'example.com'))
        result = Record.split_data('10 100 1 example.com')
        self.assertEqual(result, (10, 100, 1, 'example.com'))

    def test_join_data(self):
        result = Record.join_data(None, None, None, 'example.com')
        self.assertEqual(result, 'example.com')
        result = Record.join_data(10, None, None, 'example.com')
        self.assertEqual(result, '10 example.com')
        result = Record.join_data(10, 100, 1, 'example.com')
        self.assertEqual(result, '10 100 1 example.com')

    def test_parse_record(self):
        result = Record.parse_record('example 3600 IN A 127.0.0.1')
        self.assertDictEqual(result, {
            'name': 'example',
            'ttl': 3600,
            'type': 'A',
            'service': None,
            'protocol': None,
            'priority': None,
            'weight': None,
            'port': None,
            'target': '127.0.0.1',
        })
