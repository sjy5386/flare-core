from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from base.views.generic import RestListView, RestDetailView
from .forms import ShortUrlForm
from .models import ShortUrl
from .providers import get_short_url_provider


@method_decorator(login_required, name='dispatch')
class ShortUrlListView(RestListView):
    title = 'Short URLs'
    url = '/api/short-urls/'


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
class ShortUrlDetailView(RestDetailView):
    title = 'Short URL detail'

    def get_url(self) -> str:
        object_id = self.kwargs['id']
        return f'/api/short-urls/{object_id}/'
