# Generated by Django 4.1.3 on 2023-01-07 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
