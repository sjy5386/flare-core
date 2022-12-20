import ipaddress

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, DeleteView

from base.views import get_remote_ip_address
from records.models import Record
from records.providers import PROVIDER_CLASS
from subdomains.models import Subdomain
from .forms import AuthenticationTokenForm
from .models import AuthenticationToken


def dynamic_dns(request: HttpRequest, token: str) -> HttpResponse:
    authentication_token = get_object_or_404(AuthenticationToken, token=token)
    if authentication_token.has_expired():
        return HttpResponse('This authentication token has expired.', status=401)
    record = authentication_token.record
    if record.type not in ('A', 'AAAA'):
        return HttpResponse('Record type is not A or AAAA.', status=400)
    if request.method == 'GET':
        return HttpResponse(record.target)
    elif request.method == 'POST':
        remote_ip_address = get_remote_ip_address(request)
        try:
            ip_address = ipaddress.ip_address(remote_ip_address)
            if not ((type(ip_address) == ipaddress.IPv4Address) and (record.type == 'A')) or not (
                    (type(ip_address) == ipaddress.IPv6Address) and (record.type == 'AAAA')):
                return HttpResponse('IP address version and record type do not match.', status=400)
        except ValueError:
            return HttpResponse('Invalid IP address.', status=400)
        if remote_ip_address == record.target:
            return HttpResponse(False)
        subdomain = get_object_or_404(Subdomain, name=record.subdomain_name, domain=record.domain)
        Record.update_record(PROVIDER_CLASS(), subdomain, record.id, target=remote_ip_address)
        return HttpResponse(remote_ip_address == record.target)
    else:
        return HttpResponse(status=405)


@method_decorator(login_required, name='dispatch')
class AuthenticationTokenListView(ListView):
    def get_queryset(self):
        return AuthenticationToken.objects.filter(record__in=Record.objects.filter(
            subdomain_name__in=map(lambda x: x.name, Subdomain.objects.filter(user=self.request.user))))


@method_decorator(login_required, name='dispatch')
class AuthenticationTokenCreateView(FormView):
    template_name = 'objects/object_form.html'
    form_class = AuthenticationTokenForm
    success_url = reverse_lazy('dynamic_dns:list')
    extra_context = {
        'title': 'Create a new authentication token',
    }

    def form_valid(self, form):
        AuthenticationToken.create(form.cleaned_data.get('name', ''), form.cleaned_data.get('record')).save()
        return super(AuthenticationTokenCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class AuthenticationTokenDeleteView(DeleteView):
    template_name = 'objects/object_confirm_delete.html'
    success_url = reverse_lazy('dynamic_dns:list')
    extra_context = {
        'title': 'Delete an authentication token',
    }

    def get_object(self, queryset=None):
        return get_object_or_404(AuthenticationToken, token=self.kwargs['token'])
