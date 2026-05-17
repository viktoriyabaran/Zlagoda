from django import forms

class CustomerCardForm(forms.Form):
    card_number = forms.CharField(max_length=13, required=True)
    cust_surname = forms.CharField(max_length=50, required=True)
    cust_name = forms.CharField(max_length=50, required=True)
    cust_patronymic = forms.CharField(max_length=50, required=False)
    phone_number = forms.CharField(max_length=13, required=True)
    city = forms.CharField(max_length=50, required=False)
    street = forms.CharField(max_length=50, required=False)
    zip_code = forms.CharField(max_length=9, required=False)
    percent = forms.IntegerField(min_value=0, required=True)

    def clean_phone_number(self):
        value = self.cleaned_data["phone_number"]
        if not value.startswith("+"):
            raise forms.ValidationError("Phone number must start with '+'")
        if len(value) > 13:
            raise forms.ValidationError("Phone number must be at most 13 characters")
        return value
