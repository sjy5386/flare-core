from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views

router = DefaultRouter()
router.register('contacts', views.ContactViewSet, basename='contact')
router.register('domains', views.DomainViewSet)
router.register('shorturls', views.ShortUrlViewSet, basename='shorturl')
router.register('subdomains', views.SubdomainViewSet, basename='subdomain')

subdomains_router = NestedDefaultRouter(router, 'subdomains', lookup='subdomain')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(subdomains_router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
