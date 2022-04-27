from django.urls import path

from . import views

app_name = 'domains'
urlpatterns = [
    path('', views.DomainListView.as_view(), name='list'),
]
