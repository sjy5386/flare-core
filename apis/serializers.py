import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from contacts.models import Contact
from subdomains.models import Subdomain


class ContactSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


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
