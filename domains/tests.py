from django.test import TestCase

from .models import Domain


def get_mock_domains(count: int = 1, **kwargs) -> list[Domain]:
    return [Domain.objects.create(**kwargs) for _ in range(count)]
