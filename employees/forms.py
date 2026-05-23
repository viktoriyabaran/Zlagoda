from django import forms

from core.forms import CHECKBOX_CLASS, LayoutForm
from core.repository import get_user_by_username

from .models import EmployeeRole
from .validators import validate_age, validate_salary

TEXT_INPUT_CLASS = "bg-transparent border border-white/50 rounded-lg px-3 py-2 w-full text-white text-sm outline-none focus:border-white"


class EmployeeForm(LayoutForm):
    empl_surname = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS})
    )
    empl_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS})
    )
    empl_patronymic = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    empl_role = forms.ChoiceField(
        choices=EmployeeRole.choices,
        widget=forms.Select(attrs={"class": TEXT_INPUT_CLASS}),
    )
    salary = forms.DecimalField(
        max_digits=13,
        decimal_places=4,
        min_value=0,
        widget=forms.NumberInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"class": TEXT_INPUT_CLASS, "type": "date"})
    )
    date_of_start = forms.DateField(
        widget=forms.DateInput(attrs={"class": TEXT_INPUT_CLASS, "type": "date"})
    )
    phone_number = forms.CharField(
        max_length=13, widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS})
    )
    city = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS})
    )
    street = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS})
    )
    zip_code = forms.CharField(
        max_length=9, widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS})
    )

    has_user_account = forms.BooleanField(
        required=False,
        label="Has user account?",
        widget=forms.CheckboxInput(
            attrs={
                "class": CHECKBOX_CLASS,
                "data-toggle-target": "extra-has_user_account",
            }
        ),
    )
    username = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    password = forms.CharField(
        max_length=128,
        required=False,
        widget=forms.PasswordInput(attrs={"class": TEXT_INPUT_CLASS}),
    )

    conditional_groups = {"has_user_account": ["username", "password"]}

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

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and get_user_by_username(username):
            raise forms.ValidationError("Username already taken")
        return username

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("has_user_account"):
            if not cleaned.get("username"):
                self.add_error("username", "Username is required")
            if not cleaned.get("password"):
                self.add_error("password", "Password is required")
        return cleaned
