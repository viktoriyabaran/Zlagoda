from .validators import validate_age

class EmployeeForm(forms.ModelForm):
    def clean_date_of_birth(self):
        value = self.cleaned_data['date_of_birth']
        validate_age(value)
        return value
