from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Region(models.Model):
    REGION_CHOICES = [
        ('Unkown', 'Unkown'),
        ('EU', 'EU'),
        ('Asia', 'Asia'),
        ('America', 'America'),
        ('Australia', 'Australia'),
        ('Africe', 'Africa'),
        ('South America', 'South America')
    ]
    region = models.CharField(max_length=20, choices=REGION_CHOICES, unique=True)

    def __str__(self):
        return self.region

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.IntegerField()
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    region = models.ManyToManyField(Region, blank=True)
