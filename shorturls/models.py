from typing import List, Optional, Tuple
from urllib.parse import urlparse

from django.db import models

from base.settings.common import AUTH_USER_MODEL
from domains.models import Domain
from .providers.base import BaseShortUrlProvider


class ShortUrl(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    domain = models.ForeignKey(Domain, on_delete=models.RESTRICT)

    name = models.CharField(max_length=63)

    short = models.CharField(max_length=31)
    long_url = models.URLField(max_length=2047)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['domain', 'short'], name='unique_domain_short'),
        ]

    @property
    def short_url(self):
        return self.join_short_url(self.domain.name, self.short)

    def __str__(self):
        return self.name

    def get_short_url(self):  # deprecated
        return self.short_url

    @classmethod
    def list_short_urls(cls, provider: Optional[BaseShortUrlProvider], user: Optional[AUTH_USER_MODEL]
                        ) -> List['ShortUrl']:
        return cls.objects.filter(user=user)

    @classmethod
    def create_short_url(cls, provider: Optional[BaseShortUrlProvider], user: Optional[AUTH_USER_MODEL],
                         **kwargs) -> 'ShortUrl':
        if provider:
            kwargs['short'] = provider.create_short_url(kwargs.get('domain'), kwargs.get('long_url'))
        short_url = cls(user=user, **kwargs)
        short_url.save()
        return short_url

    @classmethod
    def retrieve_short_url(cls, provider: Optional[BaseShortUrlProvider], user: Optional[AUTH_USER_MODEL],
                           id: int) -> 'ShortUrl':
        return cls.objects.get(id=id, user=user)

    @staticmethod
    def split_short_url(short_url: str) -> Tuple[str, str]:
        parsed_url = urlparse(short_url)
        return parsed_url.netloc, parsed_url.path[1:]

    @staticmethod
    def join_short_url(domain_name: str, short: str) -> str:
        return f'https://{domain_name}/{short}'
