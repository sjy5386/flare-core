import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

import records.providers
from contacts.models import Contact
from records.models import Record
from shorturls.models import ShortUrl
from subdomains.models import Subdomain


class ShortUrlSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    short_url = serializers.URLField(read_only=True)

    class Meta:
        model = ShortUrl
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'short']


class SubdomainSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    expiry = serializers.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=90), read_only=True)
    full_name = serializers.SerializerMethodField()

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

    def get_fields(self):
        fields = super(SubdomainSerializer, self).get_fields()
        request = self.context.get('request')
        contacts = Contact.objects.filter(user=request.user)
        fields.update({
            'registrant': serializers.PrimaryKeyRelatedField(queryset=contacts),
            'admin': serializers.PrimaryKeyRelatedField(queryset=contacts),
            'tech': serializers.PrimaryKeyRelatedField(queryset=contacts),
            'billing': serializers.PrimaryKeyRelatedField(queryset=contacts),
        })
        return fields

    def get_full_name(self, obj):
        return str(obj)


class RecordSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    data = serializers.CharField(read_only=True)
    subdomain = serializers.CharField(read_only=True)

    class Meta:
        model = Record
        exclude = ('provider_id', 'subdomain_name', 'domain',)
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        provider = records.providers.get_dns_record_provider(validated_data.get('subdomain').domain)
        return Record.create_dns_record(provider, **validated_data)

    def update(self, instance, validated_data):
        provider = records.providers.get_dns_record_provider(validated_data.get('subdomain').domain)
        return Record.update_dns_record(provider, id=instance.id, **validated_data)
