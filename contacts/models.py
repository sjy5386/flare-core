from django.db import models

from base.settings.common import AUTH_USER_MODEL
from .validators import validate_country, validate_phone


class Contact(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=63)
    organization = models.CharField(max_length=63, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=31)
    state_province = models.CharField(max_length=31)
    postal_code = models.CharField(max_length=7)
    country = models.CharField(max_length=2, validators=[validate_country])
    phone = models.CharField(max_length=15, validators=[validate_phone])
    fax = models.CharField(max_length=15, blank=True, validators=[validate_phone])
    email = models.EmailField()

    def to_whois(self, is_private: bool = False,
                 contact_url: str = '', public_fields: list[str] = ()) -> dict[str, str]:
        data_redacted_message = 'DATA REDACTED'
        return {
            'name': data_redacted_message if is_private and 'name' not in public_fields else self.name,
            'organization': data_redacted_message if is_private and 'organization' not in public_fields else self.organization,
            'street': data_redacted_message if is_private and 'street' not in public_fields else self.street,
            'city': data_redacted_message if is_private and 'city' not in public_fields else self.city,
            'state_province': data_redacted_message if is_private and 'state_province' not in public_fields else self.state_province,
            'postal_code': data_redacted_message if is_private and 'postal_code' not in public_fields else self.postal_code,
            'country': data_redacted_message if is_private and 'country' not in public_fields and 'country' not in public_fields else self.country,
            'phone': data_redacted_message if is_private and 'phone' not in public_fields else self.phone,
            'fax': data_redacted_message if is_private and 'fax' not in public_fields else self.fax,
            'email': contact_url if is_private and 'email' not in public_fields and contact_url else data_redacted_message if is_private else self.email,
        }

    def __str__(self):
        return self.name
