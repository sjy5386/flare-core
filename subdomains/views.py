from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import SubdomainForm
from .models import Subdomain


@method_decorator(login_required, name='dispatch')
class SubdomainListView(ListView):
    template_name = 'subdomains/list.html'

    def get_queryset(self):
        return Subdomain.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class SubdomainCreateView(CreateView):
    template_name = 'subdomains/create.html'
    form_class = SubdomainForm
    success_url = reverse_lazy('subdomain_list')

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
