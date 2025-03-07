# Generated by Django 5.1.6 on 2025-02-21 10:52

import contacts.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=63)),
                ('organization', models.CharField(blank=True, max_length=63)),
                ('street', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=31)),
                ('state_province', models.CharField(max_length=31)),
                ('postal_code', models.CharField(max_length=7)),
                ('country', models.CharField(max_length=2, validators=[contacts.validators.validate_country])),
                ('phone', models.CharField(max_length=15, validators=[contacts.validators.validate_phone])),
                ('fax', models.CharField(blank=True, max_length=15, validators=[contacts.validators.validate_phone])),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
