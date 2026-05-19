from django import forms

from .services import CategoryService

TEXT_INPUT_CLASS = "bg-transparent border border-white/50 rounded-lg px-3 py-2 w-full text-white text-sm outline-none focus:border-white"


class CategoryForm(forms.Form):
    category_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS})
    )


class ProductForm(forms.Form):
    id_product = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": TEXT_INPUT_CLASS})
    )
    category_number = forms.ChoiceField(
        choices=[], widget=forms.Select(attrs={"class": TEXT_INPUT_CLASS})
    )
    product_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS})
    )
    characteristics = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = CategoryService().get_all()
        self.fields["category_number"].choices = [
            (c["id"], c["category_name"]) for c in categories
        ]
