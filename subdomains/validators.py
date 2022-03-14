import re

from django.core.exceptions import ValidationError


def validate_domain_name(value):
    if not re.match('^[a-z0-9][a-z0-9-]*[a-z0-9]$', value.lower()):
        raise ValidationError('This is an invalid name.')
