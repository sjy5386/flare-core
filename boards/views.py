from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from .forms import PostForm
from .models import Board, Post


class PostListView(ListView):
    def get_queryset(self):
        return Post.objects.filter(board__name=self.kwargs['board_name'])


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    form_class = PostForm
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.board = get_object_or_404(Board, name=self.kwargs['board_name'])
        post.user = self.request.user
        post.save()
        return super(PostCreateView, self).form_valid(form)
