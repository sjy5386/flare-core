from django.urls import path

from . import views

urlpatterns = [
    path('', views.ContactListView.as_view(), name='contact_list'),
    path('create/', views.ContactCreateView.as_view(), name='contact_create'),
    path('<int:id>/', views.ContactDetailView.as_view(), name='contact_detail'),
    path('<int:id>/update/', views.ContactUpdateView.as_view(), name='contact_update'),
]
