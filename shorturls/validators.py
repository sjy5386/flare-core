from django.core.exceptions import ValidationError


def validate_filter_long_url(value):
    from .models import Filter
    if not Filter.filter_all(value):
        raise ValidationError('This string is not allowed.')
