import os
from typing import Any

import requests

from domains.models import Domain
from .base import BaseShortUrlProvider
from ..exceptions import ShortUrlProviderError


class BitlyShortUrlProvider(BaseShortUrlProvider):
    host = 'https://api-ssl.bitly.com'
    token = os.environ.get('BITLY_ACCESS_TOKEN')
    headers = {
        'Authorization': f'Bearer {token}',
    }

    def list_short_urls(self, domain: Domain) -> list[dict[str, Any]]:
        raise ShortUrlProviderError()

    def create_short_url(self, domain: Domain, **kwargs) -> dict[str, Any]:
        response = requests.post(self.host + '/v4/shorten', headers=self.headers, json={
            'long_url': kwargs.get('long_url'),
            'domain': domain.name,
        })
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise ShortUrlProviderError(response.json())
        from shorturls.models import ShortUrl
        return {
            'short': ShortUrl.split_short_url(response.json().get('link'))[-1],
        }

    def retrieve_short_url(self, domain: Domain, short: str) -> dict[str, Any] | None:
        raise ShortUrlProviderError()

    def update_short_url(self, domain: Domain, short: str, **kwargs) -> dict[str, Any]:
        raise ShortUrlProviderError()

    def delete_short_url(self, domain: Domain, short: str) -> None:
        raise ShortUrlProviderError()

    def get_hostname(self, domain: Domain) -> str:
        return 'cname.bitly.com'
