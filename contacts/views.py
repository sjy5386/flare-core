from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import ContactForm
from .models import Contact


@method_decorator(login_required, name='dispatch')
class ContactListView(ListView):
    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class ContactCreateView(CreateView):
    template_name = 'objects/object_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts:list')
    extra_context = {
        'title': 'Create a new contact',
    }

    def form_valid(self, form):
        contact = form.save(commit=False)
        contact.user = self.request.user
        contact.save()
        return super(ContactCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ContactDetailView(DetailView):
    template_name = 'objects/object_detail.html'
    extra_context = {
        'title': 'Contact detail',
    }

    def get_object(self, queryset=None):
        return model_to_dict(get_object_or_404(Contact, id=self.kwargs['id'], user=self.request.user),
                             exclude=('user',))


@method_decorator(login_required, name='dispatch')
class ContactUpdateView(UpdateView):
    template_name = 'objects/object_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts:list')
    extra_context = {
        'title': 'Update a contact',
    }

    def get_object(self, queryset=None):
        return get_object_or_404(Contact, id=self.kwargs['id'], user=self.request.user)


@method_decorator(login_required, name='dispatch')
class ContactDeleteView(DeleteView):
    template_name = 'objects/object_confirm_delete.html'
    success_url = reverse_lazy('contacts:list')
    extra_context = {
        'title': 'Delete a contact',
    }

    def get_object(self, queryset=None):
        return get_object_or_404(Contact, id=self.kwargs['id'], user=self.request.user)
