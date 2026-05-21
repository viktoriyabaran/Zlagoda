from django.core.validators import MinValueValidator
from django.db import models

from customers.models import CustomerCard
from employees.models import Employee


class Check(models.Model):
    check_number = models.CharField(max_length=10, primary_key=True)
    id_employee = models.ForeignKey(
        Employee,
        on_delete=models.DO_NOTHING,
        db_column="id_employee",
    )
    card_number = models.ForeignKey(
        CustomerCard,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        db_column="card_number",
    )
    print_date = models.DateTimeField()
    sum_total = models.DecimalField(
        max_digits=13, decimal_places=4, validators=[MinValueValidator(0)]
    )
    vat = models.DecimalField(
        max_digits=13, decimal_places=4, validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"Check {self.check_number}: {self.sum_total} by {self.id_employee} on {self.print_date}"


class Sale(models.Model):
    pk = models.CompositePrimaryKey("UPC", "check_number")
    UPC = models.ForeignKey(
        "products.StoreProduct",
        on_delete=models.DO_NOTHING,
        db_column="UPC",
    )
    check_number = models.ForeignKey(
        Check,
        on_delete=models.CASCADE,
        db_column="check_number",
    )
    product_number = models.IntegerField(validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(
        max_digits=13, decimal_places=4, validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"Sale {self.UPC}, check {self.check_number}: {self.product_number} for {self.selling_price}"
