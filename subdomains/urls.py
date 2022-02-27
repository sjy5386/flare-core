from django.urls import path

from . import views

urlpatterns = [
    path('', views.SubdomainListView.as_view(), name='subdomain_list'),
    path('search/', views.search, name='subdomain_search'),
    path('create/', views.SubdomainCreateView.as_view(), name='subdomain_create'),
    path('<int:id>/', views.SubdomainDetailView.as_view(), name='subdomain_detail'),
    path('<int:id>/update/', views.SubdomainUpdateView.as_view(), name='subdomain_update'),
    path('<int:id>/delete/', views.SubdomainDeleteView.as_view(), name='subdomain_delete'),
]
