from django.db import models


class Board(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=63)
    title = models.CharField(max_length=255)
