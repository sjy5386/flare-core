from rest_framework import serializers

from .models import ShortUrl


class ShortUrlSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ShortUrl
        fields = (
            'uuid',
            'created_at',
            'updated_at',
            'user',
            'domain_uuid',
            'domain_name',
            'name',
            'short',
            'long_url',
            'short_url',
        )
        read_only_fields = (
            'uuid',
            'created_at',
            'updated_at',
            'short',
            'short_url',
        )
