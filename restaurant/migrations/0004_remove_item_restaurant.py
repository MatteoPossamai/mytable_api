# Generated by Django 4.1.3 on 2023-01-16 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_restaurant_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='restaurant',
        ),
    ]