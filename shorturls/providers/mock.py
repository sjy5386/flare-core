import base64
import random
from typing import Any

from domains.models import Domain
from .base import BaseShortUrlProvider


class MockShortUrlProvider(BaseShortUrlProvider):
    def list_short_urls(self, domain: Domain) -> list[dict[str, Any]]:
        return []

    def create_short_url(self, domain: Domain, **kwargs) -> dict[str, Any]:
        long_url = kwargs.get('long_url')
        return {
            'short': base64.urlsafe_b64encode(long_url.encode()).decode()[:random.randint(4, 8)],
        }

    def retrieve_short_url(self, domain: Domain, short: str) -> dict[str, Any] | None:
        return {
            'short': short,
        }

    def update_short_url(self, domain: Domain, short: str, **kwargs) -> dict[str, Any]:
        return kwargs

    def delete_short_url(self, domain: Domain, short: str) -> None:
        pass

    def get_hostname(self, domain: Domain) -> str:
        return 'example.com'
