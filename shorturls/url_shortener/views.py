from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_GET

from ..models import ShortUrl


@require_GET
def redirect_to_long_url(request: HttpRequest, short: str):
    domain__name = request.META.get('HTTP_HOST')
    short_url = get_object_or_404(ShortUrl, domain__name=domain__name, short=short)
    return redirect(short_url.long_url)
