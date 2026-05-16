from django import forms
from .models import Category


class CategoryForm(forms.Form):
    category_name = forms.CharField(required=True)
