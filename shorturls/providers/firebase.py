import os
from typing import Dict, Any

import requests

from domains.models import Domain
from .base import BaseShortUrlProvider


class FirebaseDynamicLinksShortUrlProvider(BaseShortUrlProvider):
    host = 'https://firebasedynamiclinks.googleapis.com'
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")

    def create_short_url(self, domain: Domain, long_url: str) -> Dict[str, Any]:
        request_body = {
            'dynamicLinkInfo': {
                'domainUriPrefix': f'https://{domain.name}',
                'link': long_url
            },
            'suffix': {
                'option': 'SHORT'
            }
        }
        response = requests.post(self.host + '/v1/shortLinks',
                                 params={'key': self.api_key}, json=request_body)
        response.raise_for_status()
        return {
            'short': response.json()['shortLink'].split('/')[-1],
        }
