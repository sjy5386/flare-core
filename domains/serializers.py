from rest_framework import serializers

from .models import Domain


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['id', 'name']
