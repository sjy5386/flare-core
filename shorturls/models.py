from typing import List, Optional, Tuple
from urllib.parse import urlparse

from django.db import models

from base.settings.common import AUTH_USER_MODEL
from domains.models import Domain
from .providers.base import BaseShortUrlProvider
from .validators import validate_filter_long_url


class ShortUrl(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    domain = models.ForeignKey(Domain, on_delete=models.RESTRICT)

    name = models.CharField(max_length=63)

    short = models.CharField(max_length=31)
    long_url = models.URLField(max_length=2047, validators=[validate_filter_long_url])

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


class Filter(models.Model):
    class FilterType(models.TextChoices):
        EQUAL = 'EQ', 'Equal'
        CONTAIN = 'CO', 'Contain'
        START_WITH = 'ST', 'Start with'
        END_WITH = 'EN', 'End with'
        REGEX = 'RE', 'Regular expression'
        URL = 'UR', 'URL'

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content = models.CharField('Content', max_length=511)
    type = models.CharField('Type', max_length=2, choices=FilterType.choices, default=FilterType.EQUAL)
    ignore_case = models.BooleanField('Ignore case', default=True)
    is_positive = models.BooleanField('Is positive', default=False)

    count = models.PositiveIntegerField('Count', default=0)

    def filter(self, target: str) -> bool:
        def f(t: str) -> bool:
            if self.type == self.FilterType.EQUAL:
                return t == self.content
            elif self.type == self.FilterType.CONTAIN:
                return self.content in t
            elif self.type == self.FilterType.START_WITH:
                return t.startswith(self.content)
            elif self.type == self.FilterType.END_WITH:
                return t.endswith(self.content)
            elif self.type == self.FilterType.REGEX:
                import re
                return bool(re.search(self.content, t))
            elif self.type == self.FilterType.URL:
                from urllib.parse import urlparse
                return urlparse(t) > urlparse(self.content)

        return not f(target.lower() if self.ignore_case else target) ^ self.is_positive

    @classmethod
    def filter_all(cls, target: str) -> bool:
        for f in cls.objects.all():
            if not f.filter(target):
                return False
        return True
