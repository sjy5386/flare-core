import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from contacts.models import Contact
from .models import Subdomain


class SubdomainSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    expiry = serializers.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=90), read_only=True)

    class Meta:
        model = Subdomain
        fields = (
            'uuid',
            'created_at',
            'updated_at',
            'user',
            'name',
            'domain',
            'domain_uuid',
            'domain_name',
            'expiry',
            'registrant',
            'admin',
            'tech',
            'billing',
            'registrant_contact_uuid',
            'admin_contact_uuid',
            'tech_contact_uuid',
            'billing_contact_uuid',
            'is_private',
            'full_name',
        )
        read_only_fields = (
            'uuid',
            'created_at',
            'updated_at',
            'expiry',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Subdomain.objects.all(),
                fields=('name', 'domain',),
            ),
        ]
        extra_kwargs = {
            'domain': {
                'write_only': True,
            },
        }

    def get_fields(self):
        fields = super(SubdomainSerializer, self).get_fields()
        request = self.context.get('request')
        contacts = Contact.objects.filter(user=request.user)
        fields.update({
            'registrant': serializers.PrimaryKeyRelatedField(queryset=contacts, write_only=True),
            'admin': serializers.PrimaryKeyRelatedField(queryset=contacts, write_only=True),
            'tech': serializers.PrimaryKeyRelatedField(queryset=contacts, write_only=True),
            'billing': serializers.PrimaryKeyRelatedField(queryset=contacts, write_only=True),
        })
        return fields
