from django.views.generic import TemplateView


class DomainListView(TemplateView):
    template_name = 'objects/object_list.html'
    extra_context = {
        'title': 'Domains',
        'url': '/api/domains/',
    }
