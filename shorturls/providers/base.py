from abc import ABCMeta, abstractmethod
from typing import Any

from domains.models import Domain


class BaseShortUrlProvider(metaclass=ABCMeta):
    @abstractmethod
    def create_short_url(self, domain: Domain, long_url: str) -> dict[str, Any]:
        pass
