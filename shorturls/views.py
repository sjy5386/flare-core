from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.generic import ListView, FormView

from .forms import ShortUrlForm
from .models import ShortUrl
from .providers import PROVIDER_CLASS


@method_decorator(login_required, name='dispatch')
class ShortUrlListView(ListView):
    template_name = 'shorturls/list.html'
    ordering = '-id'

    def get_queryset(self):
        provider = PROVIDER_CLASS()
        return ShortUrl.list_short_urls(provider, self.request.user).order_by(self.get_ordering())


@method_decorator(login_required, name='dispatch')
class ShortUrlCreateView(FormView):
    template_name = 'shorturls/create.html'
    form_class = ShortUrlForm
    success_url = reverse_lazy('shorturls:list')

    def form_valid(self, form):
        provider = PROVIDER_CLASS()
        ShortUrl.create_short_url(provider, self.request.user, **form.cleaned_data)
        return super(ShortUrlCreateView, self).form_valid(form)


@login_required
@require_GET
def detail_short_url(request, id: int):
    return render(request, 'shorturls/detail.html', {
        'object': get_object_or_404(ShortUrl, id=id, user=request.user)
    })
