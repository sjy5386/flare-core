import os
from typing import Dict, Any

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

    def create_short_url(self, domain: Domain, long_url: str) -> Dict[str, Any]:
        response = requests.post(self.host + '/v4/shorten', headers=self.headers, json={
            'long_url': long_url,
            'domain': domain.name,
        })
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise ShortUrlProviderError(response.json())
        return {
            'short': response.json().get('link').split('/')[-1]
        }
