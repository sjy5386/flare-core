from django.contrib.auth.decorators import login_required
from django.forms import Form
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, DetailView

from base.views.generic import RestDetailView
from subdomains.models import Subdomain
from .forms import DnsRecordForm, ZoneImportForm
from .models import Record
from .providers import get_dns_record_provider


@method_decorator(login_required, name='dispatch')
class DnsRecordListView(ListView):
    template_name = 'records/dns_record_list.html'
    context_object_name = 'records'
    ordering = 'type', 'name', '-id'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subdomain = None

    def dispatch(self, request, *args, **kwargs):
        self.subdomain = get_object_or_404(Subdomain, uuid=kwargs['subdomain_id'], user=request.user)
        return super(DnsRecordListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        provider = get_dns_record_provider(self.subdomain.domain)
        records = Record.list_dns_records(provider, self.subdomain)
        self.subdomain.records = len(records)
        self.subdomain.save()
        return records

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DnsRecordListView, self).get_context_data(**kwargs)
        context.update({
            'subdomain': self.subdomain
        })
        return context


@method_decorator(login_required, name='dispatch')
class DnsRecordCreateView(FormView):
    template_name = 'records/dns_record_create.html'
    form_class = DnsRecordForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subdomain = None

    def dispatch(self, request, *args, **kwargs):
        self.subdomain = get_object_or_404(Subdomain, uuid=kwargs['subdomain_id'], user=request.user)
        return super(DnsRecordCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DnsRecordCreateView, self).get_context_data(**kwargs)
        context.update({
            'subdomain': self.subdomain,
        })
        return context

    def get_initial(self):
        return {
            'name': self.subdomain.name,
        }

    def form_valid(self, form):
        provider = get_dns_record_provider(self.subdomain.domain)
        Record.create_dns_record(provider, self.subdomain, **form.cleaned_data)
        return super(DnsRecordCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('records:list', kwargs=self.kwargs)


@method_decorator(login_required, name='dispatch')
class DnsRecordDetailView(RestDetailView):
    title = 'DNS Record detail'

    def get_url(self) -> str:
        subdomain_id = self.kwargs['subdomain_id']
        object_id = self.kwargs['id']
        return f'/api/subdomains/{subdomain_id}/dns-records/{object_id}/'


@method_decorator(login_required, name='dispatch')
class DnsRecordUpdateView(FormView):
    template_name = 'records/dns_record_update.html'
    form_class = DnsRecordForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subdomain = None
        self.record = None

    def dispatch(self, request, *args, **kwargs):
        self.subdomain = get_object_or_404(Subdomain, uuid=kwargs['subdomain_id'], user=request.user)
        self.record = get_object_or_404(Record, uuid=kwargs['id'])
        return super(DnsRecordUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DnsRecordUpdateView, self).get_context_data(**kwargs)
        context.update({
            'subdomain': self.subdomain,
            'record': self.record,
        })
        return context

    def get_initial(self):
        return {
            'name': self.record.name,
            'ttl': self.record.ttl,
            'type': self.record.type,
            'service': self.record.service,
            'protocol': self.record.protocol,
            'priority': self.record.priority,
            'weight': self.record.weight,
            'port': self.record.port,
            'target': self.record.target,
        }

    def get_form_kwargs(self):
        kwargs = super(DnsRecordUpdateView, self).get_form_kwargs()
        kwargs.update({
            'readonly_fields': ['name', 'type', 'service', 'protocol'],
        })
        return kwargs

    def form_valid(self, form):
        provider = get_dns_record_provider(self.subdomain.domain)
        Record.update_dns_record(provider, self.subdomain, self.record.id, **form.cleaned_data)
        return super(DnsRecordUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('records:list', kwargs={'subdomain_id': self.kwargs['subdomain_id']})


@method_decorator(login_required, name='dispatch')
class DnsRecordDeleteView(FormView):
    template_name = 'objects/object_confirm_delete.html'
    form_class = Form
    extra_context = {
        'title': 'Delete a record',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subdomain = None
        self.record = None

    def dispatch(self, request, *args, **kwargs):
        self.subdomain = get_object_or_404(Subdomain, uuid=kwargs['subdomain_id'], user=request.user)
        self.record = get_object_or_404(Record, uuid=kwargs['id'])
        return super(DnsRecordDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DnsRecordDeleteView, self).get_context_data(**kwargs)
        context.update({
            'object': self.record,
        })
        return context

    def form_valid(self, form):
        provider = get_dns_record_provider(self.subdomain.domain)
        Record.delete_dns_record(provider, self.subdomain, self.record.id)
        return super(DnsRecordDeleteView, self).form_valid(form)

    def get_success_url(self):
        return reverse('records:list', kwargs={'subdomain_id': self.kwargs['subdomain_id']})


@method_decorator(login_required, name='dispatch')
class ZoneExportView(DetailView):
    template_name = 'records/zone_export.html'
    context_object_name = 'zone'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subdomain = None

    def dispatch(self, request, *args, **kwargs):
        self.subdomain = get_object_or_404(Subdomain, uuid=kwargs['subdomain_id'], user=request.user)
        return super(ZoneExportView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        provider = get_dns_record_provider(self.subdomain.domain)
        return Record.export_zone(provider, self.subdomain)

    def get_context_data(self, **kwargs):
        context = super(ZoneExportView, self).get_context_data(**kwargs)
        context.update({
            'subdomain': self.subdomain,
        })
        return context


@method_decorator(login_required, name='dispatch')
class ZoneImportView(FormView):
    template_name = 'objects/object_form.html'
    form_class = ZoneImportForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subdomain = None

    def dispatch(self, request, *args, **kwargs):
        self.subdomain = get_object_or_404(Subdomain, uuid=kwargs['subdomain_id'], user=request.user)
        return super(ZoneImportView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ZoneImportView, self).get_context_data(**kwargs)
        context.update({
            'subdomain': self.subdomain,
            'title': f'Import zone {self.subdomain}',
        })
        return context

    def form_valid(self, form):
        provider = get_dns_record_provider(self.subdomain.domain)
        zone = form.cleaned_data.get('zone', '')
        Record.import_zone(provider, self.subdomain, zone)
        return super(ZoneImportView, self).form_valid(form)

    def get_success_url(self):
        return reverse('records:list', kwargs=self.kwargs)
