import ast
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView

from accounts.models import User
from base.views import get_remote_ip_address
from .forms import PostForm, CommentForm
from .models import Board, Post, Comment


class BoardListView(ListView):
    model = Board


class PostListView(ListView):
    ordering = '-id'
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, name=kwargs['board_name'])
        if not User.check_permission(request.user, board.list_permission):
            messages.add_message(request, messages.ERROR, 'You do not have permission.')
            return redirect(reverse('board_list'))
        return super(PostListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(board__name=self.kwargs['board_name']).order_by(self.get_ordering())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['board'] = get_object_or_404(Board, name=self.kwargs['board_name'])
        return context


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    template_name = 'boards/post_create.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, name=kwargs['board_name'])
        if not User.check_permission(request.user, board.write_permission):
            messages.add_message(request, messages.ERROR, 'You do not have permission.')
            return redirect(reverse('post_list', kwargs=kwargs))
        return super(PostCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        board = get_object_or_404(Board, name=kwargs['board_name'])
        if not User.check_permission(request.user, board.write_permission):
            messages.add_message(request, messages.ERROR, 'You do not have permission.')
            return redirect(reverse('post_list', kwargs=kwargs))
        if not request.user.is_staff:
            last_post = Post.objects.filter(board=board, user=request.user).last()
            if last_post and (last_post.created_at + datetime.timedelta(minutes=5) > datetime.datetime.now(
                    tz=datetime.timezone.utc) and last_post.title == request.POST['title'] and last_post.content ==
                              request.POST['content']):
                return redirect(reverse('post_list', kwargs=kwargs))
        return super(PostCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.board = get_object_or_404(Board, name=self.kwargs['board_name'])
        post.user = self.request.user
        post.ip_address = get_remote_ip_address(self.request)
        post.save()
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('post_list', kwargs=self.kwargs)


class PostDetailView(DetailView, FormView):
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, name=kwargs['board_name'])
        if not User.check_permission(request.user, board.read_permission):
            messages.add_message(request, messages.ERROR, 'You do not have permission.')
            return redirect(reverse('post_detail', kwargs=kwargs))
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        post_id = kwargs['id']
        views = request.COOKIES.get('views', [])
        if type(views) is str:
            views = ast.literal_eval(views)
        if post_id not in views:
            views.append(post_id)
        response.set_cookie('views', views)
        return response

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['id'], board__name=self.kwargs['board_name'])
        if not User.check_permission(request.user, post.board.comment_permission):
            messages.add_message(request, messages.ERROR, 'You do not have permission.')
            return redirect(reverse('post_detail', kwargs=kwargs))
        if not request.user.is_staff:
            last_comment = Comment.objects.filter(post=post, user=request.user).last()
            if last_comment and (last_comment.created_at + datetime.timedelta(minutes=5) > datetime.datetime.now(
                    tz=datetime.timezone.utc) and last_comment.content == request.POST['content']):
                return redirect(reverse('post_detail', kwargs=kwargs))
        return super(PostDetailView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, id=self.kwargs['id'], board__name=self.kwargs['board_name'])
        views = ast.literal_eval(self.request.COOKIES.get('views', '[]'))
        if post.id not in views:
            post.views += 1
        post.comments = len(Comment.objects.filter(post=post))
        post.save()
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        board = get_object_or_404(Board, name=self.kwargs['board_name'])
        context['board'] = board
        context['comments'] = Comment.objects.filter(post_id=self.kwargs['id'])
        context['comment_permission'] = User.check_permission(self.request.user, board.comment_permission)
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = get_object_or_404(Post, id=self.kwargs['id'])
        comment.user = self.request.user
        comment.ip_address = get_remote_ip_address(self.request)
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
