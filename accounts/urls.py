from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.register, name='register'),
    path('oauth/', include('social_django.urls', namespace='social')),
]
