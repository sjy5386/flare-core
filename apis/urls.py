from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register('contacts', views.ContactViewSet)
router.register('domains', views.DomainViewSet)
router.register('shorturls', views.ShortUrlViewSet, basename='shorturl')
router.register('subdomains', views.SubdomainViewSet)

subdomains_router = NestedDefaultRouter(router, 'subdomains', lookup='subdomain')
subdomains_router.register('records', views.RecordViewSet, basename='record')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(subdomains_router.urls)),
    path('auth/', include('rest_framework.urls')),
]
