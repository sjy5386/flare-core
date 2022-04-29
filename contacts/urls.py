from django.urls import path

from . import views

app_name = 'contacts'
urlpatterns = [
    path('', views.ContactListView.as_view(), name='list'),
    path('create/', views.ContactCreateView.as_view(), name='create'),
    path('<int:id>/', views.ContactDetailView.as_view(), name='detail'),
    path('<int:id>/update/', views.ContactUpdateView.as_view(), name='update'),
    path('<int:id>/delete/', views.ContactDeleteView.as_view(), name='delete'),
]
