# Generated by Django 5.0.2 on 2024-05-10 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_rename_user_order_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer',
            new_name='user',
        ),
    ]
