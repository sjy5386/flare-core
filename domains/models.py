from django.db import models


class Domain(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    records_provider_id = models.CharField(max_length=255, null=True)
    shorturls_provider_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
