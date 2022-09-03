from django.urls import path

from . import views

app_name = 'shorturls'
urlpatterns = [
    path('', views.ShortUrlListView.as_view(), name='list'),
    path('create/', views.ShortUrlCreateView.as_view(), name='create'),
    path('<int:id>/', views.detail_short_url, name='detail'),
]
