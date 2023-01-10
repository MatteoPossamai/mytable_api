# Generated by Django 4.1.3 on 2023-01-10 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_remove_category_iconid_category_description_and_more'),
        ('accounts', '0002_restaurantuser_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantuser',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
    ]
