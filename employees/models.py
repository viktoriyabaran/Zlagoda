from django.db import models


class EmployeeRole(models.TextChoices):
    MANAGER = "Manager", "Manager"
    CASHIER = "Cashier", "Cashier"
