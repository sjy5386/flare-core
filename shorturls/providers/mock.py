import base64
import random
from typing import Any

from domains.models import Domain
from .base import BaseShortUrlProvider


class MockShortUrlProvider(BaseShortUrlProvider):
    def list_short_urls(self, domain: Domain) -> list[dict[str, Any]]:
        return []

    def create_short_url(self, domain: Domain, long_url: str) -> dict[str, Any]:
        return {
            'short': base64.urlsafe_b64encode(long_url.encode()).decode()[:random.randint(4, 8)],
        }

    def retrieve_short_url(self, domain: Domain, short: str) -> dict[str, Any] | None:
        return {
            'short': short,
        }
