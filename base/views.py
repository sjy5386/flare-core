from django.http import HttpRequest
from django.shortcuts import render

from contacts.models import Contact
from shorturls.forms import ShortUrlLiteForm
from shorturls.models import ShortUrl
from subdomains.forms import SubdomainSearchLiteForm
from subdomains.models import Subdomain


def index(request: HttpRequest):
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
