from django.core.mail import send_mail
from django.urls import reverse

from base.settings.common import DEFAULT_FROM_EMAIL


def send_validation(strategy, backend, code, partial_token):
    url = strategy.request.build_absolute_uri('{}?verification_code={}&partial_token={}'.format(
        reverse('social:complete', args=(backend.name,)), code.code, partial_token
    ))
    send_mail(
        'Validate your account',
        f'Validate your account {url}',
        DEFAULT_FROM_EMAIL,
        [code.email],
        fail_silently=False,
    )
