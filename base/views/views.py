import os

from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET

from ..geoip import MaxMindGeoIpWebServicesClient
from ..settings import BASE_DIR
from contacts.models import Contact
from shorturls.forms import ShortUrlLiteForm
from shorturls.models import ShortUrl
from subdomains.forms import SubdomainSearchLiteForm
from subdomains.models import Subdomain


@require_GET
def index(request: HttpRequest) -> HttpResponse:
    context = {
        'subdomain_form': SubdomainSearchLiteForm(),
        'short_url_form': ShortUrlLiteForm(),
    }
    if request.user.is_authenticated:
        context.update({
            'subdomains': Subdomain.objects.filter(user=request.user),
            'contacts': Contact.objects.filter(user=request.user),
            'shorturls': ShortUrl.objects.filter(user=request.user),
        })
    return render(request, 'index.html', context)


@cache_page(86400)
@require_GET
def favicon_ico(request: HttpRequest) -> HttpResponse:
    filename = BASE_DIR / 'favicon.ico'
    if not os.path.isfile(filename):
        raise Http404('The favicon.ico file cannot be found.')
    f = open(filename, 'rb')
    content = f.read()
    f.close()
    return HttpResponse(content, content_type='image/x-icon')


@cache_page(86400)
@require_GET
def robots_txt(request: HttpRequest) -> HttpResponse:
    filename = BASE_DIR / 'robots.txt'
    if not os.path.isfile(filename):
        raise Http404('The robot.txt file cannot be found.')
    f = open(filename, 'r')
    content = f.read()
    f.close()
    return HttpResponse(content, content_type='text/plain')


@require_GET
def what_is_my_ip_address(request: HttpRequest) -> HttpResponse:
    from base.templates.context_processors import remote_ip_address
    ip_address = remote_ip_address(request).get('remote_ip_address')
    client = MaxMindGeoIpWebServicesClient()
    info = client.lookup(ip_address)
    return render(request, 'what_is_my_ip_address.html', {
        'info': info,
    })
