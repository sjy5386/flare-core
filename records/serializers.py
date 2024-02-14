from rest_framework import serializers

from . import providers
from .models import Record


class RecordSerializer(serializers.ModelSerializer):
    subdomain = serializers.CharField(read_only=True)

    class Meta:
        model = Record
        fields = (
            'uuid',
            'created_at',
            'updated_at',
            'subdomain_name',
            'domain',
            'domain_uuid',
            'domain_name',
            'name',
            'ttl',
            'type',
            'service',
            'protocol',
            'priority',
            'weight',
            'port',
            'target',
            'full_name',
            'data',
            'subdomain',
        )
        read_only_fields = (
            'uuid',
            'created_at',
            'updated_at',
            'full_name',
            'data',
        )

    def create(self, validated_data):
        provider = providers.get_dns_record_provider(validated_data.get('subdomain').domain)
        return Record.create_dns_record(provider, **validated_data)

    def update(self, instance, validated_data):
        provider = providers.get_dns_record_provider(validated_data.get('subdomain').domain)
        return Record.update_dns_record(provider, id=instance.id, **validated_data)
