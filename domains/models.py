from django.db import models

from base.settings.common import AUTH_USER_MODEL
from records.providers import DnsRecordProvider
from shorturls.providers import ShortUrlProvider


class Domain(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.RESTRICT)  # Domain registrant or administrator
    is_public = models.BooleanField(default=False)

    dns_record_provider = models.CharField(max_length=63, choices=[(x.name, x) for x in DnsRecordProvider])
    short_url_provider = models.CharField(max_length=63, choices=[(x.name, x) for x in ShortUrlProvider])

    def __str__(self):
        return self.name
