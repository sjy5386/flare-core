from django.contrib import admin

from .models import ShortUrl, BlockedDomain

admin.site.register(ShortUrl)
admin.site.register(BlockedDomain)
