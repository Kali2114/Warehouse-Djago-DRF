# Generated by Django 5.0 on 2024-02-06 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouseapp', '0008_region_product_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='region',
            field=models.CharField(choices=[('Unkown', 'Unkown'), ('EU', 'EU'), ('Asia', 'Asia'), ('America', 'America'), ('Australia', 'Australia'), ('Africa', 'Africa'), ('South America', 'South America')], max_length=20, unique=True),
        ),
    ]