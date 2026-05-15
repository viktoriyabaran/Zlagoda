from django.db import models


# Define Category, Product, StoreProduct models here
class Category(models.Model):
    category_number = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=50)


class Product(models.Model):
    id_product = models.IntegerField(primary_key=True)
    category_number = models.ForeignKey(
        Category, on_delete=models.RESTRICT, db_column="category_number"
    )
    product_name = models.CharField(max_length=50)
    characteristics = models.CharField(max_length=100)
