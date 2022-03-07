from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import PostForm
from .models import Board, Post


class BoardListView(ListView):
    model = Board


class PostListView(ListView):
    def get_queryset(self):
        return Post.objects.filter(board__name=self.kwargs['board_name'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['board'] = get_object_or_404(Board, name=self.kwargs['board_name'])
        return context


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    template_name = 'boards/post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.board = get_object_or_404(Board, name=self.kwargs['board_name'])
        post.user = self.request.user
        post.save()
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('post_list', kwargs=self.kwargs)


class PostDetailView(DetailView):
    def get_object(self, queryset=None):
        post = get_object_or_404(Post, id=self.kwargs['id'], board__name=self.kwargs['board_name'])
        user = self.request.user
        if post.is_private and (not user.is_authenticated or post.user != user or not user.is_staff):
            raise Http404('This post is private.')
        return post


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    form_class = PostForm
    success_url = reverse_lazy('post_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Post, id=self.kwargs['id'], board__name=self.kwargs['board_name'],
                                 user=self.request.user)


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    success_url = reverse_lazy('post_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Post, id=self.kwargs['id'], board__name=self.kwargs['board_name'],
                                 user=self.request.user)
