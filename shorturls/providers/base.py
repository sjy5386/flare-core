from typing import Dict, Any

from domains.models import Domain


class BaseShortUrlProvider:
    def create_short_url(self, domain: Domain, long_url: str) -> Dict[str, Any]:
        pass
