from django.http import HttpRequest

from base.settings.common import SITE_NAME, SITE_DOMAIN_NAME


def site_name(request: HttpRequest) -> dict[str, str]:
    return {
        'site_name': SITE_NAME,
        'site_domain_name': SITE_DOMAIN_NAME if SITE_DOMAIN_NAME else request.META.get('HTTP_HOST', 'subshorts.com'),
    }
