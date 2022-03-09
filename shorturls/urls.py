from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_short_urls, name='shorturl_list'),
    path('create/', views.create_short_url, name='shorturl_create'),
]
