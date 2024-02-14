import uuid
from django.db import models


class Report(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    your_name = models.CharField(max_length=63)
    your_email = models.EmailField()

    abusive_subdomain_name_or_short_url = models.CharField(max_length=255)

    subject = models.CharField(max_length=63)
    body = models.TextField()

    def __str__(self):
        return self.subject
