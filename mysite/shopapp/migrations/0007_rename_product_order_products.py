# Generated by Django 5.0.6 on 2024-05-13 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0006_order_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='products',
        ),
    ]