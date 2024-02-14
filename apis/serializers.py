from rest_framework import serializers

import records.providers
import records.providers
from records.models import Record


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
