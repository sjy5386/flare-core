from django.urls import path

from . import views

app_name = 'contacts'
urlpatterns = [
    path('', views.ContactListView.as_view(), name='list'),
    path('create/', views.ContactCreateView.as_view(), name='create'),
    path('<str:id>/', views.ContactDetailView.as_view(), name='detail'),
    path('<str:id>/update/', views.ContactUpdateView.as_view(), name='update'),
    path('<str:id>/delete/', views.ContactDeleteView.as_view(), name='delete'),
]
