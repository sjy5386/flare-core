import base64
import random
from typing import Dict, Any

from domains.models import Domain
from .base import BaseShortUrlProvider


class MockShortUrlProvider(BaseShortUrlProvider):
    def create_short_url(self, domain: Domain, long_url: str) -> Dict[str, Any]:
        return {
            'short': base64.urlsafe_b64encode(long_url.encode()).decode()[:random.randint(4, 8)],
        }
