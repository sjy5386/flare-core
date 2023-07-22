import datetime

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

import records.providers
import shorturls.providers
from base.settings.common import SITE_NAME
from contacts.models import Contact
from domains.models import Domain
from records.models import Record
from shorturls.models import ShortUrl
from subdomains.models import Subdomain
from .serializers import ContactSerializer, DomainSerializer, ShortUrlSerializer, SubdomainSerializer, RecordSerializer

schema_view = get_schema_view(
    openapi.Info(
        title=f'{SITE_NAME} API',
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated]
)


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class DomainViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [permissions.IsAuthenticated]


class ShortUrlViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ShortUrlSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        provider = shorturls.providers.get_short_url_provider(None)
        return ShortUrl.list_short_urls(provider, self.request.user)


class SubdomainViewSet(viewsets.ModelViewSet):
    serializer_class = SubdomainSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subdomain.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(expiry=datetime.datetime.now() + datetime.timedelta(days=90))

    def perform_update(self, serializer):
        serializer.save(expiry=datetime.datetime.now() + datetime.timedelta(days=90))


@api_view(['GET'])
def whois(request: Request) -> Response:
    q = request.GET.get('q', '')
    result = Subdomain.whois(q)
    if result is None:
        return Response({'message': 'No match for "' + q + '".'}, status=404)
    return Response(result)


class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subdomain = None

    def dispatch(self, request, *args, **kwargs):
        self.subdomain = get_object_or_404(Subdomain, pk=kwargs['subdomain_pk'])
        return super(RecordViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        provider = records.providers.get_record_provider(self.subdomain.domain)
        return Record.list_records(provider, self.subdomain)

    def perform_create(self, serializer):
        serializer.save(subdomain=self.subdomain)

    def perform_update(self, serializer):
        serializer.save(subdomain=self.subdomain)

    def perform_destroy(self, instance):
        provider = records.providers.get_record_provider(self.subdomain.domain)
        Record.delete_record(provider, self.subdomain, instance.id)
