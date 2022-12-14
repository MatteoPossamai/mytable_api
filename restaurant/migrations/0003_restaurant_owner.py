# Generated by Django 4.1.3 on 2023-01-10 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_baseuser_alter_restaurantuser_options_and_more'),
        ('restaurant', '0002_remove_category_iconid_category_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='owner',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='restaurants', to='accounts.restaurantuser'),
            preserve_default=False,
        ),
    ]
