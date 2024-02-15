from rest_framework import serializers

from .models import Domain


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = (
            'uuid',
            'created_at',
            'updated_at',
            'name',
        )
        read_only_fields = (
            'uuid',
            'created_at',
            'updated_at',
        )
