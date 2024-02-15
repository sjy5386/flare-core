import uuid
from django.db import models


class WebForwarding(models.Model):
    class HttpStatusCodeRedirection(models.IntegerChoices):
        MOVED_PERMANENTLY = 301
        FOUND = 302

    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    domain_name = models.CharField(max_length=255)

    destination_url = models.URLField('Destination URL')
    http_status_code = models.IntegerField('HTTP Status Code', choices=HttpStatusCodeRedirection.choices)
    force_path_root = models.BooleanField('Force path root?')


class DomainParking(models.Model):
    uuid = models.UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    domain_name = models.CharField(max_length=255)

    title = models.CharField('Title', max_length=63, blank=True)
    content = models.TextField('Content', blank=True)
