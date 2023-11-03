from enum import Enum

from domains.models import Domain
from .base import BaseShortUrlProvider
from .bitly import BitlyShortUrlProvider
from .firebase import FirebaseDynamicLinksShortUrlProvider


class ShortUrlProvider(Enum):
    BITLY = (BitlyShortUrlProvider,)
    FIREBASE_DYNAMIC_LINKS = (FirebaseDynamicLinksShortUrlProvider,)

    def __init__(self, provider_class: type[BaseShortUrlProvider]):
        self.provider_class = provider_class


def get_short_url_provider(domain: Domain | None) -> BaseShortUrlProvider | None:
    if domain is None:
        return None
    return ShortUrlProvider[domain.short_url_provider].provider_class()
