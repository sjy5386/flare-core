from django.urls import path

from . import views

app_name = 'subdomains'
urlpatterns = [
    path('', views.SubdomainListView.as_view(), name='list'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('whois/', views.WhoisView.as_view(), name='whois'),
    path('contact/', views.SubdomainContactView.as_view(), name='contact'),
    path('create/', views.SubdomainCreateView.as_view(), name='create'),
    path('<uuid:id>/', views.SubdomainDetailView.as_view(), name='detail'),
    path('<uuid:id>/update/', views.SubdomainUpdateView.as_view(), name='update'),
    path('<uuid:id>/delete/', views.SubdomainDeleteView.as_view(), name='delete'),
]
