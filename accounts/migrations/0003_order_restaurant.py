# Generated by Django 5.0.2 on 2024-05-08 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20240508_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.restaurantprofile'),
        ),
    ]
