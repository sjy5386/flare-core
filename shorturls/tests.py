from django.test import TestCase

from .models import ShortUrl, Filter


class ShortUrlTest(TestCase):
    def test_split_short_url(self):
        result = ShortUrl.split_short_url('https://example.com/index')
        self.assertEqual(result, ('example.com', 'index'))

    def test_join_short_url(self):
        result = ShortUrl.join_short_url('example.com', 'index')
        self.assertEqual(result, 'https://example.com/index')


class FilterTest(TestCase):
    def test_filter(self):
        filter_ = Filter(content='example', type=Filter.FilterType.EQUAL)
        result = filter_.filter('example')
        self.assertEqual(result, False)
        result = filter_.filter('my example')
        self.assertEqual(result, True)
        filter_.type = Filter.FilterType.CONTAIN
        result = filter_.filter('This is an example.')
        self.assertEqual(result, False)
        result = filter_.filter('e x a m p l e')
        self.assertEqual(result, True)
