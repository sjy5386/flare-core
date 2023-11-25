from base.views.generic import RestView


class DomainListView(RestView):
    template_name = 'objects/object_list.html'
    title = 'Domains'
    url = '/api/domains/'
