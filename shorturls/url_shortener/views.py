from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET

from ..models import ShortUrl


@require_GET
def redirect_to_long_url(request: HttpRequest, short: str) -> HttpResponse:
    domain__name = request.META.get('HTTP_HOST')
    short_url = get_object_or_404(ShortUrl, domain__name=domain__name, short=short)
    return redirect(short_url.long_url)


@require_GET
def qrcode(request: HttpRequest, short: str) -> HttpResponse:
    domain__name = request.META.get('HTTP_HOST')
    short_url = get_object_or_404(ShortUrl, domain__name=domain__name, short=short)
    return render(request, 'shorturls/url_shortener/qrcode.html', {
        'object': short_url,
    })
