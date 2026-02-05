"""
Core models - used ONLY for schema generation via migrations.
All queries must use raw SQL from core.db module.
"""
from django.db import models


class UserRole(models.TextChoices):
    MANAGER = 'Manager', 'Manager'
    CASHIER = 'Cashier', 'Cashier'
