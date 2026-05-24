from django.db import models

from core.roles import Role


class EmployeeRole(models.TextChoices):
    MANAGER = Role.MANAGER, Role.MANAGER
    CASHIER = Role.CASHIER, Role.CASHIER


class Employee(models.Model):
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

    def __str__(self):
        return f"{self.empl_surname} {self.empl_name}: {self.empl_role}"
