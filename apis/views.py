import datetime

from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from contacts.models import Contact
from domains.models import Domain
from shorturls.models import ShortUrl
from subdomains.models import Subdomain
from .serializers import ContactSerializer, DomainSerializer, ShortUrlSerializer, SubdomainSerializer, RecordSerializer


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
        return ShortUrl.objects.filter(user=self.request.user)


class SubdomainViewSet(viewsets.ModelViewSet):
    serializer_class = SubdomainSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subdomain.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(expiry=datetime.datetime.now() + datetime.timedelta(days=90))

    def perform_update(self, serializer):
        serializer.save(expiry=datetime.datetime.now() + datetime.timedelta(days=90))


class RecordViewSet(viewsets.ViewSet):
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        obj = serializer.save()
        provider = self.get_provider()
        subdomain = get_object_or_404(Subdomain, pk=self.kwargs['subdomain_pk'])
        provider.create_record(subdomain, obj)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        obj = serializer.save()
        provider = self.get_provider()
        subdomain = get_object_or_404(Subdomain, pk=self.kwargs['subdomain_pk'])
        provider.update_record(subdomain, obj.identifier, obj)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        provider = self.get_provider()
        subdomain = get_object_or_404(Subdomain, pk=self.kwargs['subdomain_pk'])
        provider.delete_record(subdomain, instance.identifier)

    def get_provider(self):
        from records.providers import PROVIDER_CLASS
        provider = PROVIDER_CLASS()
        return provider

    def get_queryset(self):
        provider = self.get_provider()
        subdomain = get_object_or_404(Subdomain, pk=self.kwargs['subdomain_pk'])
        queryset = provider.list_records(subdomain)
        return queryset

    def get_object(self):
        provider = self.get_provider()
        subdomain = get_object_or_404(Subdomain, pk=self.kwargs['subdomain_pk'])
        obj = provider.retrieve_record(subdomain, self.kwargs['pk'])
        if obj is None:
            raise NotFound
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
