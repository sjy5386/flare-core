from django.views.generic import ListView

from .models import Domain


class DomainListView(ListView):
    queryset = Domain.objects.filter(is_active=True, is_public=True)
