import datetime

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView

from domains.models import Domain
from .forms import SubdomainForm, SubdomainSearchForm, SubdomainWhoisForm, SubdomainContactForm
from .models import Subdomain, ReservedName


@method_decorator(login_required, name='dispatch')
class SubdomainListView(ListView):
    template_name = 'subdomains/list.html'

    def get_queryset(self):
        return Subdomain.objects.filter(user=self.request.user)


@require_GET
def search(request):
    q = request.GET.get('q', '')
    domain = request.GET.getlist('domain', list(map(lambda e: e.id, Domain.objects.filter(is_active=True))))
    hide_unavailable = (lambda x: x == 'on')(request.GET.get('hide_unavailable', 'off'))
    results = {}
    for domain_id in domain:
        subdomain = q + '.' + Domain.objects.get(id=domain_id).name
        is_available = len(Subdomain.objects.filter(name=q, domain_id=domain_id)) == 0 and len(
            ReservedName.objects.filter(name=q)) == 0
        if is_available or not hide_unavailable:
            results[subdomain] = is_available
    return render(request, 'subdomains/search.html', {
        'form': SubdomainSearchForm(initial={
            'q': q,
            'domain': domain,
            'hide_unavailable': hide_unavailable
        }),
        'results': results.items()
    })


@require_GET
def whois(request):
    q = request.GET.get('q', '')
    subdomain = None
    if '.' in q:
        i = q.index('.')
        name = q[:i]
        domain__name = q[i + 1:]
        try:
            subdomain = Subdomain.objects.get(name=name, domain__name=domain__name)
            if subdomain.is_private:
                def make_contact_url(contact):
                    return f'{reverse_lazy("subdomain_contact")}?subdomain={subdomain.__str__()}&contact={contact}'

                subdomain.registrant.redact_data(is_registrant=True, email=make_contact_url('registrant'))
                subdomain.admin.redact_data(email=make_contact_url('admin'))
                subdomain.tech.redact_data(email=make_contact_url('tech'))
                subdomain.billing.redact_data(email=make_contact_url('billing'))
        except Subdomain.DoesNotExist:
            pass
    return render(request, 'subdomains/whois.html', {
        'form': SubdomainWhoisForm(initial={
            'q': q,
        }),
        'object': subdomain
    })


class SubdomainContactView(FormView):
    template_name = 'subdomains/contact.html'
    form_class = SubdomainContactForm
    success_url = reverse_lazy('subdomain_contact')

    def get_initial(self):
        return {
            'subdomain_name': self.request.GET.get('subdomain', ''),
            'contacts': self.request.GET.getlist('contact', [])
        }

    def form_valid(self, form):
        subdomain_name = form.cleaned_data.get('subdomain_name')
        if '.' in subdomain_name:
            i = subdomain_name.index('.')
            name = subdomain_name[:i]
            domain__name = subdomain_name[i + 1:]
            subdomain = get_object_or_404(Subdomain, name=name, domain__name=domain__name)
            contacts = form.cleaned_data.get('contacts')
            recipient_list = set()
            if 'registrant' in contacts:
                recipient_list.add(subdomain.registrant.email)
            if 'admin' in contacts:
                recipient_list.add(subdomain.admin.email)
            if 'tech' in contacts:
                recipient_list.add(subdomain.tech.email)
            if 'billing' in contacts:
                recipient_list.add(subdomain.billing.email)
            recipient_list = list(recipient_list)
            EmailMessage(
                subject=form.cleaned_data.get('subject'),
                body=form.cleaned_data.get('message'),
                to=recipient_list,
                reply_to=[form.cleaned_data.get('your_email')]
            ).send(fail_silently=True)
        return super(SubdomainContactView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class SubdomainCreateView(CreateView):
    template_name = 'subdomains/create.html'
    success_url = reverse_lazy('subdomain_list')
    form_class = SubdomainForm

    def get_form_kwargs(self):
        kwargs = super(SubdomainCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        return {
            'name': self.request.GET.get('name', ''),
            'domain': self.request.GET.get('domain', None)
        }

    def form_valid(self, form):
        subdomain = form.save(commit=False)
        if len(ReservedName.objects.filter(name=subdomain.name)) == 0:
            subdomain.user = self.request.user
            subdomain.expiry = datetime.datetime.now() + datetime.timedelta(days=90)
            subdomain.registrant = form.cleaned_data['registrant']
            subdomain.admin = form.cleaned_data['admin']
            subdomain.tech = form.cleaned_data['tech']
            subdomain.billing = form.cleaned_data['billing']
            subdomain.save()
        return super(SubdomainCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class SubdomainDetailView(DetailView):
    template_name = 'subdomains/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Subdomain, id=self.kwargs['id'], user=self.request.user)


@method_decorator(login_required, name='dispatch')
class SubdomainUpdateView(UpdateView):
    template_name = 'subdomains/update.html'
    form_class = SubdomainForm
    success_url = reverse_lazy('subdomain_list')

    def get_form_kwargs(self):
        kwargs = super(SubdomainUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        return get_object_or_404(Subdomain, id=self.kwargs['id'], user=self.request.user)

    def form_valid(self, form):
        subdomain = form.save(commit=False)
        subdomain.expiry = datetime.datetime.now() + datetime.timedelta(days=90)
        subdomain.save()
        return super(SubdomainUpdateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class SubdomainDeleteView(DeleteView):
    template_name = 'subdomains/delete.html'
    success_url = reverse_lazy('subdomain_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Subdomain, id=self.kwargs['id'], user=self.request.user)
