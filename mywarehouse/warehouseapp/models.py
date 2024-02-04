from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.IntegerField()
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)

