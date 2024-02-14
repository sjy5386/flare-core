from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contact
        fields = (
            'uuid',
            'created_at',
            'updated_at',
            'user',
            'name',
            'organization',
            'street',
            'city',
            'state_province',
            'postal_code',
            'country',
            'phone',
            'fax',
            'email',
        )
        read_only_fields = (
            'uuid',
            'created_at',
            'updated_at',
        )
