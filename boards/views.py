from django.views.generic import ListView

from .models import Post


class PostListView(ListView):
    def get_queryset(self):
        return Post.objects.filter(board__name=self.kwargs['board_name'])
