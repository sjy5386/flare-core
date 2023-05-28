from django.contrib.auth import get_user_model
from django.test import TestCase

from base.settings.common import AUTH_USER_MODEL


def get_mock_users(count: int = 1, **kwargs) -> list[AUTH_USER_MODEL]:
    return [get_user_model().objects.create_user(**kwargs) for _ in range(count)]
