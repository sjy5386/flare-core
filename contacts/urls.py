from django.urls import path

from . import views

urlpatterns = [
    path('', views.ContactListView.as_view(), name='contact_list'),
    path('create/', views.ContactCreateView.as_view(), name='contact_create'),
]
