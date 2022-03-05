from django.db import models

from subshorts.settings import AUTH_USER_MODEL


class Board(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=63)
    title = models.CharField(max_length=255)


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    title = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False)
    content = models.TextField()

    views = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    content = models.TextField()
    is_private = models.BooleanField(default=False)
