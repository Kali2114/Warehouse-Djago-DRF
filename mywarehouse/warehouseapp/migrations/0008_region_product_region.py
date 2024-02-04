# Generated by Django 5.0 on 2024-02-04 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouseapp', '0007_alter_company_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(choices=[('Unkown', 'Unkown'), ('EU', 'EU'), ('Asia', 'Asia'), ('America', 'America'), ('Australia', 'Australia'), ('Africe', 'Africa'), ('South America', 'South America')], max_length=20, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='region',
            field=models.ManyToManyField(blank=True, to='warehouseapp.region'),
        ),
    ]
