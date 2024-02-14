from rest_framework import serializers

from .models import ShortUrl


class ShortUrlSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    short_url = serializers.URLField(read_only=True)

    class Meta:
        model = ShortUrl
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'short']
