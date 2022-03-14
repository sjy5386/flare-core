import re

from django.core.exceptions import ValidationError


def validate_phone(value):
    if not re.match('\+\d{1,3}\.\d+', value):
        raise ValidationError('Please your phone number. e.g. +1.1234567890')
