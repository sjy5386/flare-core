from django.test import TestCase

from accounts.tests import get_mock_users
from .models import Domain


def get_mock_domains(count: int = 1, **kwargs) -> list[Domain]:
    return [Domain.objects.create(**kwargs) for _ in range(count)]


class DomainTest(TestCase):
    def setUp(self) -> None:
        self.user = get_mock_users(
            username='carol', password='test', email='carol@example.com',
            first_name='Carol', last_name='Test',
        )[0]
        self.domain = get_mock_domains(
            name='example.com',
            user=self.user,
        )[0]

    def test_list_domains(self):
        result = Domain.objects.filter(user=self.user)
        self.assertIn(self.domain, result)
