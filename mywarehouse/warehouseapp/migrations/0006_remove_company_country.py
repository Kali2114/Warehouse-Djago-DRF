# Generated by Django 5.0 on 2024-01-07 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouseapp', '0005_company_country_product_company_alter_company_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='country',
        ),
    ]
