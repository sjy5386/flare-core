from django.urls import path

from . import views

app_name = 'shorturls'
urlpatterns = [
    path('', views.list_short_urls, name='list'),
    path('create/', views.create_short_url, name='create'),
    path('<int:id>/', views.detail_short_url, name='detail'),
]
