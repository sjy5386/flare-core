from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, DetailView

from .exceptions import ShortUrlNotFoundError
from .forms import ShortUrlForm
from .models import ShortUrl
from .providers import get_short_url_provider


@method_decorator(login_required, name='dispatch')
class ShortUrlListView(ListView):
    ordering = '-id'

    def get_queryset(self):
        provider = get_short_url_provider(None)
        return ShortUrl.list_short_urls(provider, self.request.user).order_by(self.get_ordering())


@method_decorator(login_required, name='dispatch')
class ShortUrlCreateView(FormView):
    template_name = 'objects/object_form.html'
    form_class = ShortUrlForm
    success_url = reverse_lazy('short_urls:list')
    extra_context = {
        'title': 'Create a new short URL',
    }

    def get_initial(self):
        return {
            'long_url': self.request.GET.get('long_url'),
        }

    def form_valid(self, form):
        provider = get_short_url_provider(form.cleaned_data.get('domain'))
        ShortUrl.create_short_url(provider, self.request.user, **form.cleaned_data)
        return super(ShortUrlCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ShortUrlDetailView(DetailView):
    template_name = 'shorturls/shorturl_detail.html'

    def get_object(self, queryset=None):
        provider = get_short_url_provider(None)
        try:
            return ShortUrl.retrieve_short_url(provider, self.request.user, self.kwargs['id'])
        except ShortUrlNotFoundError as e:
            raise Http404(e)
