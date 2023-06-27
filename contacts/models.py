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
        def is_private_field(k: str) -> bool:
            return is_private and k not in public_fields

        def redact_data(whois: dict[str, str], message: str = 'DATA REDACTED') -> dict[str, str]:
            for k in whois.keys():
                if is_private_field(k):
                    whois[k] = message
                    if k == 'email' and contact_url is not None:
                        whois[k] = contact_url
            return whois

        return redact_data({
            'name': self.name,
            'organization': self.organization,
            'street': self.street,
            'city': self.city,
            'state_province': self.state_province,
            'postal_code': self.postal_code,
            'country': self.country,
            'phone': self.phone,
            'fax': self.fax,
            'email': self.email,
        })

    def __str__(self):
        return self.name
