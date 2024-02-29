import datetime
import secrets

import uuid
from django.db import models

from records.models import Record


class AuthenticationToken(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=63, blank=True)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    token = models.CharField(primary_key=True, max_length=32)
    expire_at = models.DateTimeField(null=True)

    def has_expired(self) -> bool:
        if self.expire_at is None:
            return False
        return self.expire_at < datetime.datetime.now(tz=datetime.timezone.utc)

    @classmethod
    def create(cls, name: str, record: Record) -> 'AuthenticationToken':
        return cls(token=secrets.token_hex(16),
                   expire_at=datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=90),
                   name=name, record=record)
