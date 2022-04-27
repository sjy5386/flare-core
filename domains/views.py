from django.views.generic import ListView

from .models import Domain


class DomainListView(ListView):
    model = Domain
