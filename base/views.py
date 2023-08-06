from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

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


@require_GET
def what_is_my_ip_address(request: HttpRequest) -> HttpResponse:
    return render(request, 'what_is_my_ip_address.html')
