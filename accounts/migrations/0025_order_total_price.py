# Generated by Django 5.0.2 on 2024-05-10 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_remove_orderitem_price_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5),
        ),
    ]
