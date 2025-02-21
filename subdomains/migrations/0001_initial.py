# Generated by Django 5.1.6 on 2025-02-21 10:52

import django.db.models.deletion
import subdomains.validators
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contacts', '0001_initial'),
        ('domains', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservedName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=63, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subdomain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=63, validators=[subdomains.validators.validate_domain_name, subdomains.validators.validate_reserved_name])),
                ('expiry', models.DateTimeField()),
                ('is_private', models.BooleanField(default=True)),
                ('records', models.PositiveIntegerField(default=0)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='admin_contact', to='contacts.contact')),
                ('billing', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='billing_contact', to='contacts.contact')),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='domains.domain')),
                ('registrant', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='registrant_contact', to='contacts.contact')),
                ('tech', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='tech_contact', to='contacts.contact')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubdomainStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('addPeriod', 'addPeriod'), ('autoRenewPeriod', 'autoRenewPeriod'), ('inactive', 'inactive'), ('ok', 'ok'), ('pendingCreate', 'pendingCreate'), ('pendingDelete', 'pendingDelete'), ('pendingRenew', 'pendingRenew'), ('pendingRestore', 'pendingRestore'), ('pendingTransfer', 'pendingTransfer'), ('pendingUpdate', 'pendingUpdate'), ('redemptionPeriod', 'redemptionPeriod'), ('renewPeriod', 'renewPeriod'), ('transferPeriod', 'transferPeriod'), ('serverDeleteProhibited', 'serverDeleteProhibited'), ('serverHold', 'serverHold'), ('serverRenewProhibited', 'serverRenewProhibited'), ('serverTransferProhibited', 'serverTransferProhibited'), ('serverUpdateProhibited', 'serverUpdateProhibited'), ('clientDeleteProhibited', 'clientDeleteProhibited'), ('clientHold', 'clientHold'), ('clientRenewProhibited', 'clientRenewProhibited'), ('clientTransferProhibited', 'clientTransferProhibited'), ('clientUpdateProhibited', 'clientUpdateProhibited')], default='ok', max_length=31)),
                ('subdomain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subdomains.subdomain')),
            ],
        ),
        migrations.AddConstraint(
            model_name='subdomain',
            constraint=models.UniqueConstraint(fields=('name', 'domain'), name='unique_domain_name'),
        ),
        migrations.AddConstraint(
            model_name='subdomainstatus',
            constraint=models.UniqueConstraint(fields=('subdomain', 'status'), name='unique_subdomain_status'),
        ),
    ]
