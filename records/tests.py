from django.test import TestCase

from .models import Record


class RecordTest(TestCase):
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
