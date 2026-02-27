from django.contrib import admin

from shop.models import Brand, Category, Product

# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)