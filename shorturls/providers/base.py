from abc import ABCMeta, abstractmethod
from typing import Any

from domains.models import Domain


class BaseShortUrlProvider(metaclass=ABCMeta):
    @abstractmethod
    def list_short_urls(self, domain: Domain) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def create_short_url(self, domain: Domain, long_url: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def retrieve_short_url(self, domain: Domain, short: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def update_short_url(self, domain: Domain, short: str, **kwargs) -> dict[str, Any]:
        pass

    @abstractmethod
    def delete_short_url(self, domain: Domain, short: str) -> None:
        pass
