from datetime import date
from django.core.exceptions import ValidationError

def validate_age(value):
    now = data.now()
    age = now.year - value.year - ((now.month, now.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("User must be at least 18 years old.")
