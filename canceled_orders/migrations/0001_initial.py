# Generated by Django 5.0.7 on 2024-07-20 19:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CanceledOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20)),
                ('order_name', models.CharField(max_length=100)),
                ('store_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('comment', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
