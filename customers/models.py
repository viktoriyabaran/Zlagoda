from django.core.validators import MinValueValidator
from django.db import models


class CustomerCard(models.Model):
    cust_surname = models.CharField(max_length=50)
    cust_name = models.CharField(max_length=50)
    cust_patronymic = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=13)
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=9, null=True, blank=True)
    percent = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Customer #{self.pk}: {self.cust_surname} {self.cust_name}"
