from django.test import TestCase

from .models import ShortUrl


class ShortUrlTest(TestCase):
    def test_split_short_url(self):
        result = ShortUrl.split_short_url('https://example.com/index')
        self.assertEqual(result, ('example.com', 'index'))

    def test_join_short_url(self):
        result = ShortUrl.join_short_url('example.com', 'index')
        self.assertEqual(result, 'https://example.com/index')
