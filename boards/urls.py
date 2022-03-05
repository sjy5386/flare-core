from django.urls import path

from . import views

urlpatterns = [
    path('<str:board_name>/', views.PostListView.as_view(), name='post_list'),
    path('<str:board_name>/create/', views.PostCreateView.as_view(), name='post_create'),
]
