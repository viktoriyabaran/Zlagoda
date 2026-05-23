from django import forms

from core.forms import LayoutForm

TEXT_INPUT_CLASS = "bg-transparent border border-white/50 rounded-lg px-3 py-2 w-full text-white text-sm outline-none focus:border-white"


class CustomerCardForm(LayoutForm):
    cust_surname = forms.CharField(
        max_length=50, required=True,
        widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    cust_name = forms.CharField(
        max_length=50, required=True,
        widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    cust_patronymic = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    phone_number = forms.CharField(
        max_length=13, required=True,
        widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    city = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    street = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    zip_code = forms.CharField(
        max_length=9, required=False,
        widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    percent = forms.IntegerField(
        min_value=0, required=True,
        widget=forms.NumberInput(attrs={"class": TEXT_INPUT_CLASS}),
    )

    def clean_phone_number(self):
        value = self.cleaned_data["phone_number"]
        if not value.startswith("+"):
            raise forms.ValidationError("Phone number must start with '+'")
        if len(value) > 13:
            raise forms.ValidationError("Phone number must be at most 13 characters")
        return value
