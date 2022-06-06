import os

import requests

from domains.models import Domain
from .base import BaseProvider


class FirebaseDynamicLinksProvider(BaseProvider):
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")

    def create_short_url(self, domain: Domain, long_url: str) -> str:
        request_body = {
            'dynamicLinkInfo': {
                'domainUriPrefix': f'https://{domain.name}',
                'link': long_url
            },
            'suffix': {
                'option': 'SHORT'
            }
        }
        response = requests.post('https://firebasedynamiclinks.googleapis.com/v1/shortLinks',
                                 params={'key': self.api_key}, json=request_body)
        return response.json()['shortLink'].split('/')[-1]
