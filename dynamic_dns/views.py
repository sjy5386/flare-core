from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView

from base.views import get_remote_ip_address
from records.models import Record
from records.providers import PROVIDER_CLASS
from subdomains.models import Subdomain
from .forms import AuthenticationTokenForm
from .models import AuthenticationToken


def dynamic_dns(request: HttpRequest, token: str) -> HttpResponse:
    authentication_token = get_object_or_404(AuthenticationToken, token=token)
    if authentication_token.has_expired():
        return HttpResponse(status=401)
    record = authentication_token.record
    if record.type not in ('A', 'AAAA'):
        return HttpResponse(status=400)
    if request.method == 'GET':
        return HttpResponse(record.target)
    elif request.method == 'POST':
        ip_address = get_remote_ip_address(request)
        if ip_address == record.target:
            return HttpResponse(False)
        subdomain = get_object_or_404(Subdomain, name=record.subdomain_name, domain=record.domain)
        Record.update_record(PROVIDER_CLASS(), subdomain, record.id, target=ip_address)
        return HttpResponse(ip_address == record.target)
    else:
        return HttpResponse(status=405)


@method_decorator(login_required, name='dispatch')
class AuthenticationTokenListView(ListView):
    def get_queryset(self):
        return AuthenticationToken.objects.filter(record__in=Record.objects.filter(
            subdomain_name__in=map(lambda x: x.name, Subdomain.objects.filter(user=self.request.user))))


@method_decorator(login_required, name='dispatch')
class AuthenticationTokenCreateView(FormView):
    template_name = 'dynamic_dns/authenticationtoken_create.html'
    form_class = AuthenticationTokenForm
    success_url = reverse_lazy('dynamic_dns:list')

    def form_valid(self, form):
        AuthenticationToken.create(form.cleaned_data.get('record')).save()
        return super(AuthenticationTokenCreateView, self).form_valid(form)
