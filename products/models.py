from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    product_name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    characteristics = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product_name} ({self.category.category_name})"


class StoreProduct(models.Model):
    UPC = models.CharField(primary_key=True, max_length=12)
    UPC_prom = models.ForeignKey(
        "products.StoreProduct", null=True, on_delete=models.SET_NULL
    )
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    selling_price = models.DecimalField(
        max_digits=13, decimal_places=4, validators=[MinValueValidator(0)]
    )
    products_number = models.IntegerField(validators=[MinValueValidator(0)])
    promotional_product = models.BooleanField()
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.product_name} for {self.selling_price}"
