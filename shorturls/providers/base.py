from abc import ABCMeta, abstractmethod
from typing import Dict, Any

from domains.models import Domain


class BaseShortUrlProvider(metaclass=ABCMeta):
    @abstractmethod
    def create_short_url(self, domain: Domain, long_url: str) -> Dict[str, Any]:
        pass
