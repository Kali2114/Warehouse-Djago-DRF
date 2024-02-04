from django.contrib import admin

from mywarehouse.warehouseapp.models import Region, Product

admin.site.register(Product)
admin.site.register(Region)
