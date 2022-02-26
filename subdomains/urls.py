from django.urls import path

from . import views

urlpatterns = [
    path('', views.SubdomainListView.as_view(), name='subdomain_list'),
    path('create/', views.SubdomainCreateView.as_view(), name='subdomain_create'),
    path('<int:id>/', views.SubdomainDetailView.as_view(), name='subdomain_detail'),
]
