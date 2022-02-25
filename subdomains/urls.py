from django.urls import path

from . import views

urlpatterns = [
    path('', views.SubdomainListView.as_view(), name='subdomain_list'),
]
