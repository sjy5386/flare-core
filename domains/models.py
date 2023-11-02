from django.db import models

from base.settings.common import AUTH_USER_MODEL


class Domain(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.RESTRICT)  # Domain registrant or administrator

    def __str__(self):
        return self.name
