import uuid
from django.db import models

from base.settings.common import AUTH_USER_MODEL


class Domain(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.RESTRICT)  # Domain registrant or administrator
    is_public = models.BooleanField(default=False)

    dns_record_provider = models.CharField(max_length=63)  # DnsRecordProvider
    short_url_provider = models.CharField(max_length=63)  # ShortUrlProvider

    def __str__(self):
        return self.name
