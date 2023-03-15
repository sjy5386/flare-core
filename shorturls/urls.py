from django.urls import path

from . import views

app_name = 'short_urls'
urlpatterns = [
    path('', views.ShortUrlListView.as_view(), name='list'),
    path('create/', views.ShortUrlCreateView.as_view(), name='create'),
    path('<int:id>/', views.ShortUrlDetailView.as_view(), name='detail'),
]
