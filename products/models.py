from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    id_product = models.IntegerField(primary_key=True)
    category_number = models.ForeignKey(Category, on_delete=models.RESTRICT)
    product_name = models.CharField(max_length=50)
    characteristics = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id_product}: {self.product_name} ({self.category_number.category_name})"
