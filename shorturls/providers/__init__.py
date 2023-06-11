from domains.models import Domain
from .base import BaseShortUrlProvider
from .firebase import FirebaseDynamicLinksShortUrlProvider

PROVIDER_CLASS = FirebaseDynamicLinksShortUrlProvider


def get_short_url_provider(domain: Domain | None) -> BaseShortUrlProvider:
    return PROVIDER_CLASS()
