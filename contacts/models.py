from django.db import models

from base.settings.common import AUTH_USER_MODEL
from .validators import validate_phone


class Contact(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=31)
    state_province = models.CharField(max_length=31)
    postal_code = models.CharField(max_length=7)
    country = models.CharField(max_length=2)
    phone = models.CharField(max_length=15, validators=[validate_phone])
    fax = models.CharField(max_length=15, blank=True, validators=[validate_phone])
    email = models.EmailField()

    def redact_data(self, message: str = 'DATA REDACTED', is_registrant: bool = False, email: str = None):
        self.name = message
        self.street = message
        self.city = message
        self.postal_code = message
        self.phone = message
        self.fax = message
        self.email = email if email else message
        if not is_registrant:
            self.organization = message
            self.state_province = message
            self.country = message

    def __str__(self):
        return self.name
