from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET

from .models import Forwarding, Parking


@require_GET
def forward(request: HttpRequest, forwarding: Forwarding = None) -> HttpResponse:
    if forwarding is None and False:
        forwarding = get_object_or_404(Forwarding, domain_name=request.META.get('HTTP_HOST'))
    destination_url = forwarding.destination_url
    if not forwarding.force_path_root:
        if destination_url.endswith('/'):
            destination_url = destination_url[:-1]
        destination_url += request.META.get('PATH_INFO') + '?' + request.META.get('QUERY_STRING')
    return redirect(destination_url,
                    permanent=forwarding.http_status_code == Forwarding.HttpStatusCodeRedirection.MOVED_PERMANENTLY)


@require_GET
def park(request: HttpRequest, parking: Parking = None) -> HttpResponse:
    if parking is None:
        parking = get_object_or_404(Parking, domain_name=request.META.get('HTTP_HOST'))
    return render(request, 'page_rules/parking.html', model_to_dict(parking))
