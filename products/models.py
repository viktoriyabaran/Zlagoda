from django.db import models

# Define Category, Product, StoreProduct models here
class Category(models.Model):
    category_number = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=50)
