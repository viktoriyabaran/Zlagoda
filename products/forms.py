from django import forms

from core.forms import CHECKBOX_CLASS, LayoutForm

from .repository import (
    get_all_categories,
    get_all_products,
    get_store_product_by_upc,
    get_store_products_by_product,
)

TEXT_INPUT_CLASS = "bg-transparent border border-white/50 rounded-lg px-3 py-2 w-full text-white text-sm outline-none focus:border-white"


class CategoryForm(LayoutForm):
    category_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS})
    )


class ProductForm(LayoutForm):
    category = forms.ChoiceField(
        choices=[], widget=forms.Select(attrs={"class": TEXT_INPUT_CLASS})
    )
    product_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS})
    )
    characteristics = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS})
    )

    add_store_product = forms.BooleanField(
        required=False,
        label="Add a store product for this product?",
        widget=forms.CheckboxInput(
            attrs={
                "class": CHECKBOX_CLASS,
                "data-toggle-target": "extra-add_store_product",
            }
        ),
    )
    upc = forms.CharField(
        max_length=12,
        required=False,
        label="UPC",
        widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    selling_price = forms.DecimalField(
        max_digits=13,
        decimal_places=4,
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={"class": TEXT_INPUT_CLASS, "step": "0.01"}),
    )
    products_number = forms.IntegerField(
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={"class": TEXT_INPUT_CLASS}),
    )

    add_promo_variant = forms.BooleanField(
        required=False,
        label="Add promotional variant?",
        widget=forms.CheckboxInput(
            attrs={
                "class": CHECKBOX_CLASS,
                "data-toggle-target": "extra-add_promo_variant",
            }
        ),
    )
    promo_upc = forms.CharField(
        max_length=12,
        required=False,
        label="Promo UPC",
        widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    promo_products_number = forms.IntegerField(
        min_value=0,
        required=False,
        label="Promo quantity",
        widget=forms.NumberInput(attrs={"class": TEXT_INPUT_CLASS}),
    )

    conditional_groups = {
        "add_store_product": [
            "upc",
            "selling_price",
            "products_number",
            "add_promo_variant",
        ],
        "add_promo_variant": ["promo_upc", "promo_products_number"],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = get_all_categories()
        self.fields["category"].choices = [
            (c["id"], c["category_name"]) for c in categories
        ]

    def clean_upc(self):
        upc = self.cleaned_data.get("upc")
        if upc and get_store_product_by_upc(upc):
            raise forms.ValidationError("UPC already exists")
        return upc

    def clean_promo_upc(self):
        promo_upc = self.cleaned_data.get("promo_upc")
        if promo_upc and get_store_product_by_upc(promo_upc):
            raise forms.ValidationError("UPC already exists")
        return promo_upc

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("add_store_product"):
            return cleaned
        for field_name in ("upc", "selling_price", "products_number"):
            if cleaned.get(field_name) in (None, ""):
                self.add_error(field_name, "Required")
        if cleaned.get("add_promo_variant"):
            for field_name in ("promo_upc", "promo_products_number"):
                if cleaned.get(field_name) in (None, ""):
                    self.add_error(field_name, "Required")
            upc = cleaned.get("upc")
            promo_upc = cleaned.get("promo_upc")
            if upc and promo_upc and upc == promo_upc:
                self.add_error("promo_upc", "Must differ from the regular UPC")
        return cleaned

class EditProductForm(LayoutForm):
    category = forms.ChoiceField(
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
        categories = get_all_categories()
        self.fields["category"].choices = [
            (c["id"], c["category_name"]) for c in categories
        ]

class StoreProductForm(LayoutForm):
    product = forms.ChoiceField(
        choices=[],
        label="Product",
        widget=forms.Select(attrs={"class": TEXT_INPUT_CLASS}),
    )
    upc = forms.CharField(
        max_length=12,
        label="UPC",
        widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    selling_price = forms.DecimalField(
        max_digits=13,
        decimal_places=4,
        min_value=0,
        widget=forms.NumberInput(attrs={"class": TEXT_INPUT_CLASS, "step": "0.01"}),
    )
    products_number = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={"class": TEXT_INPUT_CLASS}),
    )

    add_promo_variant = forms.BooleanField(
        required=False,
        label="Add promotional variant?",
        widget=forms.CheckboxInput(
            attrs={
                "class": CHECKBOX_CLASS,
                "data-toggle-target": "extra-add_promo_variant",
            }
        ),
    )
    promo_upc = forms.CharField(
        max_length=12,
        required=False,
        label="Promo UPC",
        widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    promo_products_number = forms.IntegerField(
        min_value=0,
        required=False,
        label="Promo quantity",
        widget=forms.NumberInput(attrs={"class": TEXT_INPUT_CLASS}),
    )

    conditional_groups = {
        "add_promo_variant": ["promo_upc", "promo_products_number"],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        products = get_all_products()
        self.fields["product"].choices = [
            (p["id"], p["product_name"]) for p in products
        ]

    def clean_product(self):
        product_id = self.cleaned_data["product"]
        if get_store_products_by_product(product_id):
            raise forms.ValidationError(
                "This product already has store products (max 2 per product)"
            )
        return product_id

    def clean_upc(self):
        upc = self.cleaned_data.get("upc")
        if upc and get_store_product_by_upc(upc):
            raise forms.ValidationError("UPC already exists")
        return upc

    def clean_promo_upc(self):
        promo_upc = self.cleaned_data.get("promo_upc")
        if promo_upc and get_store_product_by_upc(promo_upc):
            raise forms.ValidationError("UPC already exists")
        return promo_upc

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("add_promo_variant"):
            for field_name in ("promo_upc", "promo_products_number"):
                if cleaned.get(field_name) in (None, ""):
                    self.add_error(field_name, "Required")
            upc = cleaned.get("upc")
            promo_upc = cleaned.get("promo_upc")
            if upc and promo_upc and upc == promo_upc:
                self.add_error("promo_upc", "Must differ from the regular UPC")
        return cleaned

class EditStoreProductForm(LayoutForm):
    selling_price = forms.DecimalField(
        max_digits=13,
        decimal_places=4,
        min_value=0,
        widget=forms.NumberInput(attrs={"class": TEXT_INPUT_CLASS, "step": "0.01"}),
    )
    products_number = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={"class": TEXT_INPUT_CLASS}),
    )
    promotional_product = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": CHECKBOX_CLASS}),
    )
