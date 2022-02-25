from django.db import models

from subshorts.settings import AUTH_USER_MODEL


class Contact(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=31)
    state_province = models.CharField(max_length=31)
    postal_code = models.CharField(max_length=7)
    country = models.CharField(max_length=2)
    phone = models.CharField(max_length=15)
    fax = models.CharField(max_length=15, blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.name
