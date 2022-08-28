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
