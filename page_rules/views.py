from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET

from .models import Parking


@require_GET
def park(request: HttpRequest, parking: Parking = None) -> HttpResponse:
    if parking is None:
        parking = get_object_or_404(Parking, domain_name=request.META.get('HTTP_HOST'))
    return render(request, 'page_rules/parking.html', model_to_dict(parking))
