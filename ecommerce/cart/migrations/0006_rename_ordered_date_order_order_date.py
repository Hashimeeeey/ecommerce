# Generated by Django 5.0.1 on 2024-03-10 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_rename_order_date_order_ordered_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='ordered_date',
            new_name='order_date',
        ),
    ]