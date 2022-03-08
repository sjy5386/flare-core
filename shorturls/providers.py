from domains.models import Domain
from .models import ShortUrl


class BaseProvider:
    def create_short_url(self, domain: Domain, name: str, long_url: str) -> ShortUrl:
        pass
