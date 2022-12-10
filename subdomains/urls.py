from django.urls import path

from . import views

app_name = 'subdomains'
urlpatterns = [
    path('', views.SubdomainListView.as_view(), name='list'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('whois/', views.whois, name='whois'),
    path('contact/', views.SubdomainContactView.as_view(), name='contact'),
    path('create/', views.SubdomainCreateView.as_view(), name='create'),
    path('<int:id>/', views.SubdomainDetailView.as_view(), name='detail'),
    path('<int:id>/update/', views.SubdomainUpdateView.as_view(), name='update'),
    path('<int:id>/delete/', views.SubdomainDeleteView.as_view(), name='delete'),
]
