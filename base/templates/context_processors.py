from django.http import HttpRequest

from base.settings.common import SITE_NAME


def site_name(request: HttpRequest) -> dict[str, str]:
    return {
        'site_name': SITE_NAME,
    }
