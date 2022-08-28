from django.urls import path

from . import views

app_name = 'reports'
urlpatterns = [
    path('create/', views.ReportCreateView.as_view(), name='create'),
]
