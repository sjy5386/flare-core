from django.contrib.auth.decorators import login_required
from django.forms import Form
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.generic import ListView, FormView, DetailView

from base.views import get_remote_ip_address
from subdomains.models import Subdomain
from . import models
from .forms import RecordForm, ZoneImportForm, RecordModelForm
from .providers import PROVIDER_CLASS
from .types import Record


@method_decorator(login_required, name='dispatch')
class RecordListView(ListView):
    context_object_name = 'records'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subdomain = None

    def dispatch(self, request, *args, **kwargs):
        self.subdomain = get_object_or_404(Subdomain, id=kwargs['subdomain_id'], user=request.user)
        return super(RecordListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        provider = PROVIDER_CLASS()
        return models.Record.list_records(provider, self.subdomain)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RecordListView, self).get_context_data(**kwargs)
        context.update({
            'subdomain': self.subdomain
        })
        return context


@method_decorator(login_required, name='dispatch')
class RecordCreateView(FormView):
    template_name = 'records/record_create.html'
    form_class = RecordModelForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subdomain = None

    def dispatch(self, request, *args, **kwargs):
        self.subdomain = get_object_or_404(Subdomain, id=kwargs['subdomain_id'], user=request.user)
        return super(RecordCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RecordCreateView, self).get_context_data(**kwargs)
        context.update({
            'subdomain': self.subdomain,
            'ip_address': get_remote_ip_address(self.request),
        })
        return context

    def get_initial(self):
        return {
            'name': self.subdomain.name
        }

    def form_valid(self, form):
        provider = PROVIDER_CLASS()
        models.Record.create_record(provider, self.subdomain, **form.cleaned_data)
        return super(RecordCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('records:list', kwargs=self.kwargs)


@method_decorator(login_required, name='dispatch')
class RecordDetailView(DetailView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subdomain = None

    def dispatch(self, request, *args, **kwargs):
        self.subdomain = get_object_or_404(Subdomain, id=kwargs['subdomain_id'], user=request.user)
        return super(RecordDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        provider = PROVIDER_CLASS()
        return models.Record.retrieve_record(provider, self.subdomain, self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(RecordDetailView, self).get_context_data(**kwargs)
        context.update({
            'subdomain': self.subdomain,
        })
        return context


@login_required
def update_record(request, subdomain_id, id):
    provider = PROVIDER_CLASS()
    subdomain = get_object_or_404(Subdomain, id=subdomain_id, user=request.user)
    if request.method == 'GET':
        record = provider.retrieve_record(subdomain, id)
        return render(request, 'records/record_update.html', {
            'subdomain': subdomain,
            'record': record,
            'form': RecordForm(initial={
                'name': record.get_name(),
                'ttl': record.ttl,
                'type': record.type,
                'service': record.service,
                'protocol': record.protocol,
                'priority': record.priority,
                'weight': record.weight,
                'port': record.port,
                'target': record.target,
            }),
            'ip_address': get_remote_ip_address(request),
        })
    elif request.method == 'POST':
        name = request.POST['name']
        ttl = request.POST['ttl']
        type = request.POST['type']
        target = request.POST['target']
        kwargs = {}
        if type == 'MX' or type == 'SRV':
            kwargs['priority'] = request.POST['priority']
        if type == 'SRV':
            kwargs['service'] = request.POST['service']
            kwargs['protocol'] = request.POST['protocol']
            kwargs['weight'] = request.POST['weight']
            kwargs['port'] = request.POST['port']
        record = Record(name, ttl, type, target, **kwargs)
        provider.update_record(subdomain, id, record)
        return redirect(reverse('records:list', kwargs={'subdomain_id': subdomain_id}))


@login_required
def delete_record(request, subdomain_id, id):
    provider = PROVIDER_CLASS()
    subdomain = get_object_or_404(Subdomain, id=subdomain_id, user=request.user)
    if request.method == 'GET':
        record = provider.retrieve_record(subdomain, id)
        return render(request, 'records/record_delete.html', {
            'subdomain': subdomain,
            'record': record,
            'form': Form()
        })
    elif request.method == 'POST':
        provider.delete_record(subdomain, id)
        return redirect(reverse('records:list', kwargs={'subdomain_id': subdomain_id}))


@login_required
@require_GET
def export_zone(request, subdomain_id):
    provider = PROVIDER_CLASS()
    subdomain = get_object_or_404(Subdomain, id=subdomain_id, user=request.user)
    zone = provider.export_zone(subdomain)
    return render(request, 'records/zone_export.html', {
        'subdomain': subdomain,
        'zone': zone
    })


@login_required
def import_zone(request, subdomain_id):
    subdomain = get_object_or_404(Subdomain, id=subdomain_id, user=request.user)
    if request.method == 'GET':
        return render(request, 'records/zone_import.html', {
            'subdomain': subdomain,
            'form': ZoneImportForm()
        })
    elif request.method == 'POST':
        provider = PROVIDER_CLASS()
        zone = request.POST['zone']
        provider.import_zone(subdomain, zone)
        return redirect(reverse('records:list', kwargs={'subdomain_id': subdomain_id}))
