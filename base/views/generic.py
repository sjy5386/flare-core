from django.views.generic import TemplateView


class RestView(TemplateView):
    title: str = ''
    url: str = ''

    def get_title(self) -> str:
        return self.title

    def get_url(self) -> str:
        return self.url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.get_title(),
            'url': self.get_url(),
        })
        return context


class RestListView(RestView):
    template_name = 'objects/object_list.html'
