from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from core.sorting import resolve_sort

from .forms import CategoryForm, ProductForm, StoreProductForm
from .services import (
    CategoryService,
    ProductService,
    StoreProductListService,
    StoreProductService,
)

CATEGORY_COLUMNS = [
    {"key": "category_name", "label": "Category", "sortable": True},
]
CATEGORY_SORTABLE = {c["key"] for c in CATEGORY_COLUMNS if c["sortable"]}


class AddCategoryView(View):
    category_service = CategoryService()

    def get(self, request):
        return render(
            request,
            "home.html",
            {
                "form": CategoryForm(),
                "form_title": "Add Category",
                "form_action": reverse("products:add-category"),
            },
        )

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            self.category_service.create(form.cleaned_data["category_name"])
            return redirect("products:categories")
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Add Category",
                "form_action": reverse("products:add-category"),
            },
        )


class GetCategoriesView(View):
    category_service = CategoryService()

    def get(self, request):
        sort_by, sort_dir = resolve_sort(
            request, CATEGORY_SORTABLE, default="category_name"
        )
        rows = self.category_service.get_all(sort_by, sort_dir)
        return render(
            request,
            "home.html",
            {
                "list": {
                    "title": "CATEGORIES",
                    "subtitle": "Product categories",
                    "rows": rows,
                    "columns": CATEGORY_COLUMNS,
                    "sort": {"by": sort_by, "dir": sort_dir},
                    "add_url": reverse("products:add-category"),
                    "add_label": "Add category",
                    "empty_message": "No categories yet.",
                },
            },
        )


PRODUCT_COLUMNS = [
    {"key": "product_name", "label": "Product Name", "sortable": True},
    {"key": "characteristics", "label": "Characteristics", "sortable": False},
    {"key": "category_name", "label": "Category", "sortable": True},
]
PRODUCT_SORTABLE = {c["key"] for c in PRODUCT_COLUMNS if c["sortable"]}


class AddProductView(View):
    product_service = ProductService()

    def get(self, request):
        return render(
            request,
            "home.html",
            {
                "form": ProductForm(),
                "form_title": "Add Product",
                "form_action": reverse("products:add-product"),
            },
        )

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            self.product_service.create(form.cleaned_data)
            return redirect("core:home")
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Add Product",
                "form_action": reverse("products:add-product"),
            },
        )


class GetProductsView(View):
    product_service = ProductService()

    def get(self, request):
        sort_by, sort_dir = resolve_sort(
            request, PRODUCT_SORTABLE, default="product_name"
        )
        rows = self.product_service.get_all(sort_by, sort_dir)

        return render(
            request,
            "home.html",
            {
                "list": {
                    "title": "PRODUCTS",
                    "subtitle": "All products available in database",
                    "rows": rows,
                    "columns": PRODUCT_COLUMNS,
                    "sort": {"by": sort_by, "dir": sort_dir},
                    "add_url": reverse("products:add-product"),
                    "add_label": "Add product",
                    "empty_message": "No products yet.",
                },
            },
        )


class AddStoreProductView(View):
    store_product_service = StoreProductService()

    def get(self, request):
        return render(
            request,
            "home.html",
            {
                "form": StoreProductForm(),
                "form_title": "Add Store Product",
                "form_action": reverse("products:add-store-product"),
            },
        )

    def post(self, request):
        form = StoreProductForm(request.POST)
        if form.is_valid():
            self.store_product_service.create(form.cleaned_data)
            return redirect("core:home")
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Add Store Product",
                "form_action": reverse("products:add-store-product"),
            },
        )


STORE_PRODUCT_COLUMNS = [
    {"key": "UPC", "label": "UPC", "sortable": False},
    {"key": "product_name", "label": "Product Name", "sortable": True},
    {"key": "selling_price", "label": "Price", "sortable": True},
    {"key": "products_number", "label": "Quantity", "sortable": True},
    {"key": "promotional_product", "label": "Promo", "sortable": False},
]
STORE_PRODUCT_SORTABLE = {c["key"] for c in STORE_PRODUCT_COLUMNS if c["sortable"]}


class GetStoreProductsView(View):
    store_product_list_service = StoreProductListService()

    def get(self, request):
        sort_by, sort_dir = resolve_sort(
            request, STORE_PRODUCT_SORTABLE, default="products_number"
        )
        rows = self.store_product_list_service.get_all(sort_by, sort_dir)
        return render(
            request,
            "home.html",
            {
                "list": {
                    "title": "STORE PRODUCTS",
                    "subtitle": "All products in store",
                    "rows": rows,
                    "columns": STORE_PRODUCT_COLUMNS,
                    "sort": {"by": sort_by, "dir": sort_dir},
                    "add_url": reverse("products:add-store-product"),
                    "add_label": "Add store product",
                    "empty_message": "No store products yet.",
                },
            },
        )
