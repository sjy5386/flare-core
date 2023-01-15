from django.urls import path, include, re_path
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
subdomains_router.register('records', views.RecordViewSet, basename='record')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(subdomains_router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('whois/', views.whois, name='whois'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', views.schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', views.schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', views.schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
