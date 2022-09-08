import base64
import random

from domains.models import Domain
from .base import BaseShortUrlProvider


class MockShortUrlProvider(BaseShortUrlProvider):
    def create_short_url(self, domain: Domain, long_url: str) -> str:
        return base64.urlsafe_b64encode(long_url.encode()).decode()[:random.randint(4, 8)]
