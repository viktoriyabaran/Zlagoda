from datetime import date

from django.core.exceptions import ValidationError


def validate_age(value):
    now = date.today()
    age = now.year - value.year - ((now.month, now.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("User must be at least 18 years old.")


def validate_salary(value):
    if value < 0:
        raise ValidationError("Salary must be a positive number")
