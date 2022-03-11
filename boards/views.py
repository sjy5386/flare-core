from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView

from .forms import PostForm, CommentForm
from .models import Board, Post, Comment


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
        post.ip_address = self.request.META['REMOTE_ADDR']
        post.save()
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('post_list', kwargs=self.kwargs)


class PostDetailView(DetailView, FormView):
    form_class = CommentForm

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, id=self.kwargs['id'], board__name=self.kwargs['board_name'])
        user = self.request.user
        if post.is_private and (not user.is_authenticated or post.user != user or not user.is_staff):
            raise Http404('This post is private.')
        post.views += 1
        post.save()
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['board'] = get_object_or_404(Board, name=self.kwargs['board_name'])
        context['comments'] = Comment.objects.filter(post_id=self.kwargs['id'])
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = get_object_or_404(Post, id=self.kwargs['id'])
        comment.user = self.request.user
        comment.ip_address = self.request.META['REMOTE_ADDR']
        comment.save()
        return super(PostDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs=self.kwargs)


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    template_name = 'boards/post_update.html'
    form_class = PostForm

    def get_object(self, queryset=None):
        return get_object_or_404(Post, id=self.kwargs['id'], board__name=self.kwargs['board_name'],
                                 user=self.request.user)

    def get_success_url(self):
        return reverse('post_detail', kwargs=self.kwargs)


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    template_name = 'boards/post_delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, id=self.kwargs['id'], board__name=self.kwargs['board_name'],
                                 user=self.request.user)

    def get_success_url(self):
        return reverse('post_list', kwargs={'board_name': self.kwargs['board_name']})
