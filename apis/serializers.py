import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from contacts.models import Contact
from domains.models import Domain
from records.types import BaseRecord, Record
from shorturls.models import ShortUrl
from subdomains.models import Subdomain


class ContactSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['id', 'name']


class ShortUrlSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ShortUrl
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'short']


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


class BaseRecordSerializer(serializers.Serializer):
    class TypeField(serializers.ChoiceField):
        def __init__(self, **kwargs):
            choices = sorted(map(lambda e: (e[0], f'{e[0]} - {e[1]}'), BaseRecord.get_available_types().items()))
            super().__init__(choices, **kwargs)

    name = serializers.CharField(max_length=255)
    ttl = serializers.IntegerField(min_value=0, max_value=65535)
    type = TypeField()
    r_type = TypeField(required=False)  # deprecated
    data = serializers.CharField()

    def create(self, validated_data):
        if 'r_type' in validated_data.keys():  # deprecated
            validated_data['type'] = validated_data['r_type']
            del validated_data['r_type']
        return BaseRecord(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.ttl = validated_data.get('ttl', instance.ttl)
        if 'r_type' in validated_data.keys():  # deprecated
            validated_data['type'] = validated_data['r_type']
            del validated_data['r_type']
        instance.type = validated_data.get('type', instance.type)
        instance.data = validated_data.get('data', instance.data)
        return instance


class RecordSerializer(BaseRecordSerializer):
    class NameField(serializers.CharField):
        def __init__(self, **kwargs):
            kwargs['source'] = '*'
            super().__init__(**kwargs)

        def to_internal_value(self, data):
            self.source_attrs = [self.field_name]
            return super().to_internal_value(data)

        def to_representation(self, value):
            if type(value) is str:
                if value[0] == '_':
                    return Record.parse_name_srv(value)[2]
                return value
            return value.get_name()

    name = NameField(max_length=255)
    full_name = serializers.SerializerMethodField()
    data = serializers.CharField(read_only=True)

    id = serializers.IntegerField(read_only=True)
    identifier = serializers.IntegerField(read_only=True, required=False)  # deprecated

    service = serializers.CharField(required=False)
    protocol = serializers.CharField(required=False)

    priority = serializers.IntegerField(min_value=0, max_value=65535, required=False)
    weight = serializers.IntegerField(min_value=0, max_value=65535, required=False)
    port = serializers.IntegerField(min_value=0, max_value=65535, required=False)

    target = serializers.CharField()

    def create(self, validated_data):
        name = validated_data.get('name')
        ttl = validated_data.get('ttl')
        if 'r_type' in validated_data.keys():  # deprecated
            validated_data['type'] = validated_data['r_type']
            del validated_data['r_type']
        type = validated_data.get('type')
        target = validated_data.get('target')
        kwargs = {}
        if type == 'MX' or type == 'SRV':
            kwargs['priority'] = validated_data.get('priority')
        if type == 'SRV':
            kwargs['service'] = validated_data.get('service')
            kwargs['protocol'] = validated_data.get('protocol')
            kwargs['weight'] = validated_data.get('weight')
            kwargs['port'] = validated_data.get('port')
        instance = Record(name, ttl, type, target, **kwargs)
        instance.identifier = instance.id  # deprecated
        return instance

    def update(self, instance, validated_data):
        instance = super(RecordSerializer, self).update(instance, validated_data)
        if 'identifier' in validated_data.keys():  # deprecated
            validated_data['id'] = validated_data['identifier']
            del validated_data['identifier']
        instance.id = validated_data.get('id', instance.id)
        instance.target = validated_data.get('target', instance.target)
        if instance.type == 'MX' or instance.type == 'SRV':
            instance.priority = validated_data.get('priority', instance.priority)
        if instance.type == 'SRV':
            instance.service = validated_data.get('service', instance.service)
            instance.protocol = validated_data.get('protocol', instance.protocol)
            instance.name = f'{instance.service}.{instance.protocol}.{instance.name}'
            instance.weight = validated_data.get('weight', instance.weight)
            instance.port = validated_data.get('port', instance.port)
        return instance

    def get_full_name(self, obj):
        return obj.name
