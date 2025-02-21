# Generated by Django 5.1.6 on 2025-02-21 10:52

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('domains', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('provider_id', models.CharField(max_length=255, null=True, unique=True)),
                ('subdomain_name', models.CharField(max_length=63)),
                ('name', models.CharField(max_length=63, verbose_name='Name')),
                ('ttl', models.IntegerField(default=3600, verbose_name='TTL')),
                ('type', models.CharField(choices=[('A', 'A - a host address'), ('NS', 'NS - an authoritative name server'), ('CNAME', 'CNAME - the canonical name for an alias'), ('MX', 'MX - mail exchange'), ('TXT', 'TXT - text strings'), ('AAAA', 'AAAA - IP6 Address'), ('SRV', 'SRV - Server Selection')], max_length=10, verbose_name='Type')),
                ('service', models.CharField(help_text='Required for SRV record.', max_length=63, null=True, verbose_name='Service')),
                ('protocol', models.CharField(help_text='Required for SRV record.', max_length=63, null=True, verbose_name='Protocol')),
                ('priority', models.IntegerField(help_text='Required for MX and SRV records.', null=True, verbose_name='Priority')),
                ('weight', models.IntegerField(help_text='Required for SRV record.', null=True, verbose_name='Weight')),
                ('port', models.IntegerField(help_text='Required for SRV record.', null=True, verbose_name='Port')),
                ('target', models.CharField(max_length=255, verbose_name='Target')),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='domains.domain')),
            ],
        ),
    ]
