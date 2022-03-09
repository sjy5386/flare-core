from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET

from domains.models import Domain
from .forms import ShortUrlForm
from .models import ShortUrl
from .providers import PROVIDER_CLASS


@login_required
@require_GET
def list_short_urls(request):
    return render(request, 'shorturls/list.html', {
        'object_list': ShortUrl.objects.filter(user=request.user)
    })


@login_required
def create_short_url(request):
    if request.method == 'GET':
        return render(request, 'shorturls/create.html', {
            'form': ShortUrlForm()
        })
    elif request.method == 'POST':
        provider = PROVIDER_CLASS()
        domain = get_object_or_404(Domain, id=request.POST['domain'])
        name = request.POST['name']
        long_url = request.POST['long_url']
        short = provider.create_short_url(domain, name, long_url)
        ShortUrl(domain=domain, name=name, short=short, long_url=long_url).save()
        return redirect(reverse('shorturl_list'))
