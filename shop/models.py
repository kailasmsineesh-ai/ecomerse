from django.db import models

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
   


class Brand(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/',default='products/default.jpg')
    CATEGORY = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    BRAND = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_rate = models.PositiveIntegerField(default=0)  
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    