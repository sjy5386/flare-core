from django.http import HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    return render(request, 'index.html')


def get_remote_ip_address(request: HttpRequest):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR'].split(', ')[0]
    else:
        return request.META['REMOTE_ADDR']
