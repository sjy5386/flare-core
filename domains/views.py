from base.views.generic import RestListView


class DomainListView(RestListView):
    title = 'Domains'
    url = '/api/domains/'
