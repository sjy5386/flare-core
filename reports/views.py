from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ReportForm


class ReportCreateView(CreateView):
    template_name = 'reports/report_create.html'
    form_class = ReportForm
    success_url = reverse_lazy('index')
