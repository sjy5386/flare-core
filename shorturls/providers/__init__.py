import os
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


DEFAULT_SHORT_URL_PROVIDER = os.environ.get('DEFAULT_SHORT_URL_PROVIDER') or ShortUrlProvider.FIREBASE_DYNAMIC_LINKS.name


def get_short_url_provider(domain: Domain | None) -> BaseShortUrlProvider:
    return ShortUrlProvider[DEFAULT_SHORT_URL_PROVIDER].provider_class()
