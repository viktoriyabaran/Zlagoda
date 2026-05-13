from django.db import models
from employees.models import Employee
from customers.models import CustomerCard
from django.core.validators import MinValueValidator

# Define Check, Sale models here
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
    sum_total = models.DecimalField(max_digits=13, decimal_places=4, validators=[MinValueValidator(0)])
    vat = models.DecimalField(max_digits=13, decimal_places=4, validators=[MinValueValidator(0)])

