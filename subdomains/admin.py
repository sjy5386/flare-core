from django.contrib import admin

from .models import Subdomain, ReservedName, SubdomainStatus

admin.site.register(Subdomain)
admin.site.register(ReservedName)
admin.site.register(SubdomainStatus)
