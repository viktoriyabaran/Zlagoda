from django.db import models

class EmployeeRole(models.TextChoices):
    MANAGER = "Manager", "Manager"
    CASHIER = "Cashier", "Cashier"

class Employee(models.Model):
    id_employee = models.CharField(max_length=10, primary_key=True)
    empl_surname = models.CharField(max_length=50)
    empl_name = models.CharField(max_length=50)
    empl_patronymic = models.CharField(max_length=50, null=True, blank=True)
    empl_role = models.CharField(max_length=10, choices=EmployeeRole.choices)
    salary = models.DecimalField(max_digits=13, decimal_places=4)
    date_of_birth = models.DateField()
    date_of_start = models.DateField()
    phone_number = models.CharField(max_length=13)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=9)


