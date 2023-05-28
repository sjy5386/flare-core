from django.test import TestCase

from .models import Contact


def get_mock_contacts(count: int = 1, **kwargs) -> list[Contact]:
    return [Contact.objects.create(**kwargs) for _ in range(count)]
