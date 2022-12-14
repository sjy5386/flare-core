from django.urls import path

from . import views

app_name = 'dynamic_dns'
urlpatterns = (
    path('<str:token>/', views.dynamic_dns, name='dynamic_dns'),
)
