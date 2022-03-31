from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from contacts.models import Contact
from domains.models import Domain
from subdomains.models import Subdomain
from .serializers import ContactSerializer, DomainSerializer, SubdomainSerializer, RecordSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [permissions.IsAdminUser]


class SubdomainViewSet(viewsets.ModelViewSet):
    queryset = Subdomain.objects.all()
    serializer_class = SubdomainSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subdomain.objects.filter(user=self.request.user)


class RecordViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, subdomain_pk):
        provider = self.get_provider()
        subdomain = get_object_or_404(Subdomain, pk=subdomain_pk)
        queryset = provider.list_records(subdomain)
        serializer = RecordSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, subdomain_pk, pk=None):
        provider = self.get_provider()
        subdomain = get_object_or_404(Subdomain, pk=subdomain_pk)
        record = provider.retrieve_record(subdomain, pk)
        serializer = RecordSerializer(record)
        return Response(serializer.data)

    def get_provider(self):
        from records.providers import PROVIDER_CLASS
        provider = PROVIDER_CLASS()
        return provider
