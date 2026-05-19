from django import forms

from .services import CategoryService


class CategoryForm(forms.Form):
    category_name = forms.CharField(required=True)


class ProductForm(forms.Form):
    id_product = forms.IntegerField()
    category_number = forms.ChoiceField(choices=[])
    product_name = forms.CharField(max_length=50)
    characteristics = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = CategoryService().get_all()
        self.fields["category_number"].choices = [
            (c["id"], c["category_name"]) for c in categories
        ]
