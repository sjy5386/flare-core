import base64
import logging
import secrets
from typing import Optional
from urllib.parse import urlparse

import uuid
from django.core.cache import cache
from django.db import models

from base.settings.common import AUTH_USER_MODEL
from domains.models import Domain
from .exceptions import ShortUrlBadRequestError, ShortUrlNotFoundError, ShortUrlProviderError
from .providers.base import BaseShortUrlProvider
from .validators import validate_filter_long_url


class ShortUrl(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=False)
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
    def short_url(self) -> str:
        return self.join_short_url(self.domain.name, self.short)

    def __str__(self):
        return self.name

    @classmethod
    def list_short_urls(cls, provider: BaseShortUrlProvider | None, user: Optional[AUTH_USER_MODEL]
                        ) -> list['ShortUrl']:
        if provider:
            try:
                pass
            except ShortUrlProviderError as e:
                logging.error(e)
        short_urls = cls.objects.filter(user=user)
        for short_url in short_urls:
            cache.set('short_urls:' + str(short_url.id), short_url, timeout=3600)
        return short_urls

    @classmethod
    def create_short_url(cls, provider: BaseShortUrlProvider | None, user: Optional[AUTH_USER_MODEL],
                         **kwargs) -> 'ShortUrl':
        for k in ('domain', 'long_url'):
            if k not in kwargs.keys():
                raise ShortUrlBadRequestError('Empty ' + k + '.')
        if provider:
            try:
                kwargs['short'] = provider.create_short_url(kwargs.get('domain'), **kwargs)['short']
            except ShortUrlProviderError as e:
                logging.error(e)
        short_url = cls(user=user, **kwargs)
        short_url.save()
        cache.set('short_urls:' + str(short_url.id), short_url, timeout=3600)
        return short_url

    @classmethod
    def retrieve_short_url(cls, provider: BaseShortUrlProvider | None, user: Optional[AUTH_USER_MODEL],
                           id: int) -> 'ShortUrl':
        cache_key = 'short_urls:' + str(id)
        cache_value = cache.get(cache_key)
        if cache_value is not None:
            return cache_value
        try:
            short_url = cls.objects.get(id=id, user=user)
            if provider:
                try:
                    pass
                except ShortUrlProviderError as e:
                    logging.error(e)
            cache.set(cache_key, short_url, timeout=3600)
            return short_url
        except cls.DoesNotExist:
            raise ShortUrlNotFoundError()

    @staticmethod
    def split_short_url(short_url: str) -> tuple[str, str]:
        parsed_url = urlparse(short_url)
        return parsed_url.netloc, parsed_url.path[1:]

    @staticmethod
    def join_short_url(domain_name: str, short: str) -> str:
        return f'https://{domain_name}/{short}'

    @staticmethod
    def create_short_by_seq(seq: int) -> str:
        return base64.urlsafe_b64encode(('%03d' % seq).encode()).decode().replace('=', '')

    @staticmethod
    def create_short_by_random(n: int = 13) -> str:
        if n < 13:
            logging.warning(f'{n} is too small.')
        return secrets.token_urlsafe(n)


class Filter(models.Model):
    class FilterType(models.TextChoices):
        EQUAL = 'EQ', 'Equal'
        CONTAIN = 'CO', 'Contain'
        START_WITH = 'ST', 'Start with'
        END_WITH = 'EN', 'End with'
        REGEX = 'RE', 'Regular expression'
        URL = 'UR', 'URL'

    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=False)
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
