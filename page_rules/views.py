from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET

from .models import WebForwarding, Parking


@require_GET
def forward_web(request: HttpRequest, web_forwarding: WebForwarding = None) -> HttpResponse:
    if web_forwarding is None and False:
        web_forwarding = get_object_or_404(WebForwarding, domain_name=request.META.get('HTTP_HOST'))
    destination_url = web_forwarding.destination_url
    if not web_forwarding.force_path_root:
        if destination_url.endswith('/'):
            destination_url = destination_url[:-1]
        destination_url += request.META.get('PATH_INFO') + '?' + request.META.get('QUERY_STRING')
    return redirect(destination_url,
                    permanent=web_forwarding.http_status_code == WebForwarding.HttpStatusCodeRedirection.MOVED_PERMANENTLY)


@require_GET
def park(request: HttpRequest, parking: Parking = None) -> HttpResponse:
    if parking is None:
        parking = get_object_or_404(Parking, domain_name=request.META.get('HTTP_HOST'))
    return render(request, 'page_rules/parking.html', model_to_dict(parking))
