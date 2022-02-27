from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from domains.models import Domain
from .forms import SubdomainForm, SubdomainSearchForm
from .models import Subdomain


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
        availability = len(Subdomain.objects.filter(name=q, domain_id=domain_id)) == 0
        if availability or not hide_unavailable:
            results[subdomain] = availability
    return render(request, 'subdomains/search.html', {
        'form': SubdomainSearchForm(initial={
            'q': q,
            'domain': domain,
            'hide_unavailable': hide_unavailable
        }),
        'results': results.items()
    })


@method_decorator(login_required, name='dispatch')
class SubdomainCreateView(CreateView):
    template_name = 'subdomains/create.html'
    form_class = SubdomainForm
    success_url = reverse_lazy('subdomain_list')

    def get_initial(self):
        return {
            'name': self.request.GET.get('name', ''),
            'domain': self.request.GET.get('domain', None)
        }

    def form_valid(self, form):
        subdomain = form.save(commit=False)
        subdomain.user = self.request.user
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

    def get_object(self, queryset=None):
        return get_object_or_404(Subdomain, id=self.kwargs['id'], user=self.request.user)


@method_decorator(login_required, name='dispatch')
class SubdomainDeleteView(DeleteView):
    template_name = 'subdomains/delete.html'
    success_url = reverse_lazy('subdomain_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Subdomain, id=self.kwargs['id'], user=self.request.user)
