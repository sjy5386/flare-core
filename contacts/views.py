from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Contact


@method_decorator(login_required, name='dispatch')
class ContactListView(ListView):
    template_name = 'contacts/list.html'

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)
