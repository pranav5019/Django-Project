# Generated by Django 5.0.1 on 2024-03-14 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('army', '0005_remove_order_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Store',
            new_name='store',
        ),
    ]
