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
        self.short_url = get_mock_short_urls(
            user=self.user,
            domain=self.domain,
            name='Test',
            short='example',
            long_url='https://example.com/',
        )[0]

    def test_list_short_urls(self):
        result = ShortUrl.list_short_urls(None, self.user)
        self.assertIn(self.short_url, result)

    def test_create_short_url(self):
        kwargs = {
            'domain': self.domain,
            'long_url': 'https://example.net/',
        }
        result = ShortUrl.create_short_url(None, self.user, **kwargs)
        for k, v in kwargs.items():
            self.assertEqual(getattr(result, k), v)

    def test_retrieve_short_url(self):
        result = ShortUrl.retrieve_short_url(None, self.user, self.short_url.id)
        self.assertEqual(result, self.short_url)

    def test_split_short_url(self):
        result = ShortUrl.split_short_url('https://example.com/index')
        self.assertEqual(result, ('example.com', 'index'))

    def test_join_short_url(self):
        result = ShortUrl.join_short_url('example.com', 'index')
        self.assertEqual(result, 'https://example.com/index')

    def test_create_short_by_seq(self):
        self.assertEqual(ShortUrl.create_short_by_seq(1), 'MDAx')
        self.assertEqual(ShortUrl.create_short_by_seq(20), 'MDIw')
        self.assertEqual(ShortUrl.create_short_by_seq(300), 'MzAw')
        self.assertEqual(ShortUrl.create_short_by_seq(4000), 'NDAwMA')
        self.assertEqual(ShortUrl.create_short_by_seq(1234567890), 'MTIzNDU2Nzg5MA')

    def test_create_short_by_random(self):
        self.assertEqual(len({ShortUrl.create_short_by_random() for _ in (range(100))}), 100)


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
