"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
import secrets

from django.contrib import admin
from django.urls import path, include

from . import views

ADMIN_URL_PREFIX = os.environ.get('ADMIN_URL_PREFIX', secrets.token_urlsafe(4))

urlpatterns = [
    path('', views.index, name='index'),
    path('robots.txt', views.robots_txt, name='robots.txt'),
    path('accounts/', include('accounts.urls')),
    path(f'{ADMIN_URL_PREFIX}/admin/', admin.site.urls),
    path('api/', include('apis.urls')),
    path('contacts/', include('contacts.urls')),
    path('domains/', include('domains.urls')),
    path('dynamic-dns/', include('dynamic_dns.urls')),
    path('reports/', include('reports.urls')),
    path('short_urls/', include('shorturls.urls')),
    path('subdomains/', include('subdomains.urls')),
    path('subdomains/<int:subdomain_id>/records/', include('records.urls')),
    path('what-is-my-ip-address/', views.what_is_my_ip_address, name='what_is_my_ip_address'),

    path('', include('shorturls.url_shortener.urls')),
]
