# Generated by Django 5.1.6 on 2025-02-21 10:52

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthenticationToken',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=63)),
                ('token', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('expire_at', models.DateTimeField(null=True)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.record')),
            ],
        ),
    ]
