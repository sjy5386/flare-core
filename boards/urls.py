from django.urls import path

from . import views

urlpatterns = [
    path('<str:board_name>/', views.PostListView.as_view(), name='post_list'),
    path('<str:board_name>/create/', views.PostCreateView.as_view(), name='post_create'),
    path('<str:board_name>/<int:id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<str:board_name>/<int:id>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('<str:board_name>/<int:id>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
