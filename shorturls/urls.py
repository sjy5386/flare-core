from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_short_urls, name='shorturl_list'),
]
