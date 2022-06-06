from domains.models import Domain


class BaseProvider:
    def create_short_url(self, domain: Domain, long_url: str) -> str:
        pass
