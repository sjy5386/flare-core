from typing import List, Optional

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
        return f'https://{self.domain.name}/{self.short}'

    def __str__(self):
        return self.name

    def get_short_url(self):  # deprecated
        return self.short_url

    @classmethod
    def list_short_urls(cls, provider: Optional[BaseShortUrlProvider], user: Optional[AUTH_USER_MODEL]
                        ) -> List['ShortUrl']:
        return cls.objects.filter(user=user)


class BlockedDomain(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    domain = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.domain
