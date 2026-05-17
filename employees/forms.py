from django import forms

from .models import EmployeeRole
from .validators import validate_age, validate_salary


class EmployeeForm(forms.ModelForm):
    id_employee = forms.CharField(max_length=10)
    empl_surname = forms.CharField(max_length=50)
    empl_name = forms.CharField(max_length=50)
    empl_patronymic = forms.CharField(max_length=50, required=False)
    empl_role = forms.ChoiceField(choices=EmployeeRole.choices)
    salary = forms.DecimalField(max_digits=13, decimal_places=4, min_value=0)
    date_of_birth = forms.DateField()
    date_of_start = forms.DateField()
    phone_number = forms.CharField(max_length=13)
    city = forms.CharField(max_length=50)
    street = forms.CharField(max_length=50)
    zip_code = forms.CharField(max_length=9)

    def clean_date_of_birth(self):
        value = self.cleaned_data["date_of_birth"]
        validate_age(value)
        return value

    def clean_salary(self):
        value = self.cleaned_data["salary"]
        validate_salary(value)
        return value

    def clean_phone_number(self):
        value = self.cleaned_data["phone_number"]
        if not value.startswith("+"):
            raise forms.ValidationError("Phone number must start with '+'")
        if len(value) > 13:
            raise forms.ValidationError("Phone number must be at most 13 characters")
        return value
