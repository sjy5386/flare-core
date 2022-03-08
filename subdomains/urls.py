from django.urls import path

from . import views

urlpatterns = [
    path('', views.SubdomainListView.as_view(), name='subdomain_list'),
    path('search/', views.search, name='subdomain_search'),
    path('whois/', views.whois, name='subdomain_whois'),
    path('contact/', views.SubdomainContactView.as_view(), name='subdomain_contact'),
    path('create/', views.SubdomainCreateView.as_view(), name='subdomain_create'),
    path('<int:id>/', views.SubdomainDetailView.as_view(), name='subdomain_detail'),
    path('<int:id>/update/', views.SubdomainUpdateView.as_view(), name='subdomain_update'),
    path('<int:id>/delete/', views.SubdomainDeleteView.as_view(), name='subdomain_delete'),

    path('<int:subdomain_id>/records/', views.list_records, name='record_list'),
    path('<int:subdomain_id>/records/create/', views.create_record, name='record_create'),
    path('<int:subdomain_id>/records/<str:identifier>/', views.retrieve_record, name='record_detail'),
]
