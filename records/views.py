from django.contrib.auth.decorators import login_required
from django.forms import Form
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET

from subdomains.models import Subdomain
from .forms import BaseRecordForm, ZoneImportForm
from .providers import PROVIDER_CLASS
from .types import Record


@login_required
@require_GET
def list_records(request, subdomain_id):
    provider = PROVIDER_CLASS()
    subdomain = get_object_or_404(Subdomain, id=subdomain_id, user=request.user)
    records = provider.list_records(subdomain)
    subdomain.records = len(records)
    subdomain.save()
    return render(request, 'records/record_list.html', {
        'subdomain': subdomain,
        'records': records
    })


@login_required
def create_record(request, subdomain_id):
    subdomain = get_object_or_404(Subdomain, id=subdomain_id, user=request.user)
    if request.method == 'GET':
        return render(request, 'records/record_create.html', {
            'subdomain': subdomain,
            'form': BaseRecordForm(initial={
                'name': subdomain.name,
            })
        })
    elif request.method == 'POST':
        provider = PROVIDER_CLASS()
        name = request.POST['name']
        ttl = request.POST['ttl']
        r_type = request.POST['r_type']
        data = request.POST['data']
        record = Record(name, ttl, r_type, data)
        provider.create_record(subdomain, record)
        return redirect(reverse('record_list', kwargs={'subdomain_id': subdomain_id}))


@login_required
@require_GET
def retrieve_record(request, subdomain_id, identifier):
    provider = PROVIDER_CLASS()
    subdomain = get_object_or_404(Subdomain, id=subdomain_id, user=request.user)
    record = provider.retrieve_record(subdomain, identifier)
    return render(request, 'records/record_detail.html', {
        'subdomain': subdomain,
        'record': record
    })


@login_required
def update_record(request, subdomain_id, identifier):
    provider = PROVIDER_CLASS()
    subdomain = get_object_or_404(Subdomain, id=subdomain_id, user=request.user)
    if request.method == 'GET':
        record = provider.retrieve_record(subdomain, identifier)
        return render(request, 'records/record_update.html', {
            'subdomain': subdomain,
            'record': record,
            'form': BaseRecordForm(initial={
                'name': record.name,
                'ttl': record.ttl,
                'r_type': record.r_type,
                'data': record.data
            })
        })
    elif request.method == 'POST':
        name = request.POST['name']
        ttl = request.POST['ttl']
        r_type = request.POST['r_type']
        data = request.POST['data']
        record = Record(name, ttl, r_type, data)
        provider.update_record(subdomain, identifier, record)
        return redirect(reverse('record_list', kwargs={'subdomain_id': subdomain_id}))


@login_required
def delete_record(request, subdomain_id, identifier):
    provider = PROVIDER_CLASS()
    subdomain = get_object_or_404(Subdomain, id=subdomain_id, user=request.user)
    if request.method == 'GET':
        record = provider.retrieve_record(subdomain, identifier)
        return render(request, 'records/record_delete.html', {
            'subdomain': subdomain,
            'record': record,
            'form': Form()
        })
    elif request.method == 'POST':
        provider.delete_record(subdomain, identifier)
        return redirect(reverse('record_list', kwargs={'subdomain_id': subdomain_id}))


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
        return redirect(reverse('record_list', kwargs={'subdomain_id': subdomain_id}))
