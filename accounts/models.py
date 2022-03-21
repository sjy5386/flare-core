from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def check_permission(user, permission):
        return [True, user.is_authenticated, user.is_staff, user.is_superuser][permission]
