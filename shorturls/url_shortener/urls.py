from django.urls import path

from . import views

app_name = 'url_shortener'
urlpatterns = (
    path('<str:short>/', views.redirect_to_long_url, name='redirect'),
)
