from rest_framework import viewsets, permissions

from contacts.models import Contact
from subdomains.models import Subdomain
from .serializers import ContactSerializer, SubdomainSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubdomainViewSet(viewsets.ModelViewSet):
    queryset = Subdomain.objects.all()
    serializer_class = SubdomainSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subdomain.objects.filter(user=self.request.user)
