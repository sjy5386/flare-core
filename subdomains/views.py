import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView

from base.views.generic import RestView
from contacts.models import Contact
from domains.models import Domain
from .forms import SubdomainForm, SubdomainSearchForm, SubdomainWhoisForm, SubdomainContactForm
from .models import Subdomain


@method_decorator(login_required, name='dispatch')
class SubdomainListView(ListView):
    ordering = 'name'

    def get_queryset(self):
        return Subdomain.objects.filter(user=self.request.user).order_by(self.get_ordering())


@method_decorator(require_GET, name='dispatch')
class SearchView(FormView, ListView):
    template_name = 'subdomains/search.html'
    form_class = SubdomainSearchForm
    context_object_name = 'results'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.q = None
        self.domain = None
        self.hide_unavailable = None

    def dispatch(self, request, *args, **kwargs):
        self.q = request.GET.get('q', '').lower()
        self.domain = request.GET.getlist('domain', list(map(lambda e: e.id, Domain.objects.filter(is_active=True))))
        self.hide_unavailable = request.GET.get('hide_unavailable', 'off') == 'on'
        return super(SearchView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'q': self.q,
            'domain': self.domain,
            'hide_unavailable': self.hide_unavailable,
        }

    def get_queryset(self):
        return Subdomain.search(self.q, Domain.objects.filter(id__in=self.domain), self.hide_unavailable)


@method_decorator(require_GET, name='dispatch')
class WhoisView(FormView, DetailView):
    template_name = 'subdomains/whois.html'
    form_class = SubdomainWhoisForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.q = None

    def dispatch(self, request, *args, **kwargs):
        self.q = request.GET.get('q', '')
        return super(WhoisView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'q': self.q
        }

    def get_object(self, queryset=None):
        return Subdomain.whois(self.q)


class SubdomainContactView(FormView):
    template_name = 'objects/object_form.html'
    form_class = SubdomainContactForm
    success_url = reverse_lazy('subdomains:contact')
    extra_context = {
        'title': 'Contact the subdomain owner',
    }

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
    template_name = 'objects/object_form.html'
    success_url = reverse_lazy('subdomains:list')
    form_class = SubdomainForm
    extra_context = {
        'title': 'Create a new subdomain',
    }

    def get(self, request, *args, **kwargs):
        if len(Contact.objects.filter(user=request.user)) == 0:
            messages.add_message(request, messages.INFO, 'Before creating a subdomain, you must create a contact.')
            return redirect(reverse('contacts:create'))
        return super(SubdomainCreateView, self).get(request, *args, **kwargs)

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
        subdomain.user = self.request.user
        subdomain.expiry = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=90)
        subdomain.registrant = form.cleaned_data['registrant']
        subdomain.admin = form.cleaned_data['admin']
        subdomain.tech = form.cleaned_data['tech']
        subdomain.billing = form.cleaned_data['billing']
        subdomain.save()
        return super(SubdomainCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class SubdomainDetailView(RestView):
    template_name = 'objects/object_detail.html'
    title = 'Subdomain detail'

    def get_url(self) -> str:
        object_id = self.kwargs['id']
        return f'/api/subdomains/{object_id}/'


@method_decorator(login_required, name='dispatch')
class SubdomainUpdateView(UpdateView):
    template_name = 'objects/object_form.html'
    form_class = SubdomainForm
    success_url = reverse_lazy('subdomains:list')
    extra_context = {
        'title': 'Update a subdomain',
    }

    def get_form_kwargs(self):
        kwargs = super(SubdomainUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        return get_object_or_404(Subdomain, uuid=self.kwargs['id'], user=self.request.user)

    def form_valid(self, form):
        subdomain = form.save(commit=False)
        subdomain.expiry = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=90)
        subdomain.save()
        return super(SubdomainUpdateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class SubdomainDeleteView(DeleteView):
    template_name = 'objects/object_confirm_delete.html'
    success_url = reverse_lazy('subdomains:list')
    extra_context = {
        'title': 'Delete a subdomain',
    }

    def get_object(self, queryset=None):
        return get_object_or_404(Subdomain, uuid=self.kwargs['id'], user=self.request.user)
