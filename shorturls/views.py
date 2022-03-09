from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import ShortUrl


@login_required
@require_GET
def list_short_urls(request):
    return render(request, 'shorturls/list.html', {
        'object_list': ShortUrl.objects.filter(user=request.user)
    })
