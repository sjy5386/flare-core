import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from contacts.models import Contact
from subdomains.models import Subdomain


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ['created_at', 'updated_at', 'user']


class SubdomainSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    expiry = serializers.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=90), read_only=True)

    class Meta:
        model = Subdomain
        exclude = ['records']
        read_only_fields = ['created_at', 'updated_at']
        validators = [
            UniqueTogetherValidator(
                queryset=Subdomain.objects.all(),
                fields=['name', 'domain'],
            ),
        ]
