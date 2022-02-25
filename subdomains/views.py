from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Subdomain


@method_decorator(login_required, name='dispatch')
class SubdomainListView(ListView):
    template_name = 'subdomains/list.html'

    def get_queryset(self):
        return Subdomain.objects.filter(user=self.request.user)
