from django.test import TestCase

from accounts.tests import get_mock_users
from domains.tests import get_mock_domains
from .models import ShortUrl, Filter


def get_mock_short_urls(count: int = 1, **kwargs) -> list[ShortUrl]:
    return [ShortUrl.objects.create(**kwargs) for _ in range(count)]


class ShortUrlTest(TestCase):
    def setUp(self) -> None:
        self.user = get_mock_users(
            username='bob', password='test', email='bob@example.com',
            first_name='Bob', last_name='Test',
        )[0]
        self.domain = get_mock_domains(name='example.com')[0]

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
