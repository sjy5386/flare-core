from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
