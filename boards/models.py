from django.db import models

from base.settings.common import AUTH_USER_MODEL


class Board(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.SlugField(unique=True)
    title = models.CharField(max_length=63)
    description = models.CharField(max_length=255, blank=True)

    list_permission = models.IntegerField(default=0)
    read_permission = models.IntegerField(default=0)
    write_permission = models.IntegerField(default=1)
    comment_permission = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    title = models.CharField(max_length=63)
    is_private = models.BooleanField(default=False)
    content = models.TextField()

    views = models.PositiveIntegerField(default=0)

    ip_address = models.GenericIPAddressField(null=True)

    comments = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title} 🔒' if self.is_private else self.title


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    content = models.TextField()
    is_private = models.BooleanField(default=False)

    ip_address = models.GenericIPAddressField(null=True)

    def __str__(self):
        return f'{self.content} 🔒' if self.is_private else self.content
