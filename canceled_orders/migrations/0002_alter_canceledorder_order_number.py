# Generated by Django 5.0.7 on 2024-07-20 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canceled_orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='canceledorder',
            name='order_number',
            field=models.CharField(max_length=50),
        ),
    ]
