import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from contacts.models import Contact
from domains.models import Domain
from subdomains.models import Subdomain
from .models import Record


class RecordTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='alice', password='test', email='alice@example.com',
            first_name='Alice', last_name='Test',
        )
        self.domain = Domain.objects.create(name='example.com')
        self.contact = Contact.objects.create(
            user=self.user,
            name='test',
            street='test',
            city='test',
            state_province='test',
            postal_code='0',
            country='US',
            phone='+1.1234567890',
            email='test@example.com',
        )
        self.subdomain = Subdomain.objects.create(
            user=self.user,
            name='test',
            domain=self.domain,
            expiry=datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=90),
            registrant=self.contact,
            admin=self.contact,
            tech=self.contact,
            billing=self.contact,
        )
        self.record = Record.objects.create(
            subdomain_name='test',
            domain=self.domain,
            name='test',
            type='A',
            target='127.0.0.1',
        )

    def test_list_records(self):
        result = Record.list_records(None, self.subdomain)
        self.assertIn(self.record, result)

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
