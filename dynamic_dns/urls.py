from django.urls import path

from . import views

app_name = 'dynamic_dns'
urlpatterns = (
    path('authentication-tokens/', views.AuthenticationTokenListView.as_view(), name='list'),
    path('authentication-tokens/create/', views.AuthenticationTokenCreateView.as_view(), name='create'),
    path('authentication-tokens/<str:token>/delete/', views.AuthenticationTokenDeleteView.as_view(), name='delete'),
    path('<str:token>/', views.dynamic_dns, name='dynamic_dns'),
)
