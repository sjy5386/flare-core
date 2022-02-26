from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from .forms import ContactForm
from .models import Contact


@method_decorator(login_required, name='dispatch')
class ContactListView(ListView):
    template_name = 'contacts/list.html'

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class ContactCreateView(CreateView):
    template_name = 'contacts/create.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_list')

    def form_valid(self, form):
        contact = form.save(commit=False)
        contact.user = self.request.user
        contact.save()
        return super(ContactCreateView, self).form_valid(form)
