import re

from django.core.exceptions import ValidationError


def validate_country(value):
    if len(value) != 2 or not re.match('[A-Z]{2}', value):
        raise ValidationError('Please enter your country code. e.g. US')


def validate_phone(value):
    if not re.match('\+\d{1,3}\.\d+', value):
        raise ValidationError('Please your phone number. e.g. +1.1234567890')
