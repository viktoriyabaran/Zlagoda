from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from core.sorting import resolve_sort

from employees.repository import resolve_filters

from .forms import (
    CategoryForm,
    EditProductForm,
    EditStoreProductForm,
    ProductForm,
    StoreProductForm,
)
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

PRODUCT_COLUMNS = [
    {"key": "product_name", "label": "Product Name", "sortable": True},
    {"key": "characteristics", "label": "Characteristics", "sortable": False},
    {"key": "category_name", "label": "Category", "sortable": True},
]
PRODUCT_SORTABLE = {c["key"] for c in PRODUCT_COLUMNS if c["sortable"]}

STORE_PRODUCT_COLUMNS = [
    {"key": "UPC", "label": "UPC", "sortable": False},
    {"key": "product_name", "label": "Product Name", "sortable": True},
    {"key": "selling_price", "label": "Price", "sortable": True},
    {"key": "products_number", "label": "Quantity", "sortable": True},
    {"key": "promotional_product", "label": "Promo", "sortable": False},
]
STORE_PRODUCT_SORTABLE = {c["key"] for c in STORE_PRODUCT_COLUMNS if c["sortable"]}

STORE_PRODUCT_FILTERS = [
    {
        "key": "promo",
        "label": "Promo Status",
        "type": "select",
        "column": "sp.promotional_product",
        "options": [
            {"value": "true", "label": "Promotional"},
            {"value": "false", "label": "Non-promotional"},
        ],
    },
]

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
                    "actions": [
                        {
                            "label": "Edit",
                            "url_name": "products:edit-category",
                            "icon": "✎",
                        },
                        {
                            "label": "Delete",
                            "url_name": "products:delete-category",
                            "icon": "✕",
                            "method": "post",
                            "confirm": "Delete this category?",
                        },
                    ],
                    "row_id_key": "id",
                },
            },
        )


class DeleteCategoryView(View):
    category_service = CategoryService()

    def post(self, request, category_id):
        try:
            self.category_service.delete(category_id)
            return HttpResponse("")
        except ValueError as e:
            return HttpResponse(str(e), status=409)

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
                    "row_id_key": "id",
                    "actions": [
                        {
                            "label": "Edit",
                            "url_name": "products:edit-product",
                            "icon": "✎",
                        },
                        {
                            "label": "Delete",
                            "url_name": "products:delete-product",
                            "icon": "✕",
                            "method": "post",
                            "confirm": "Delete this product?",
                        },
                    ],
                },
            },
        )


class EditProductView(View):
    product_service = ProductService()

    def get(self, request, product_id):
        product = self.product_service.get_by_id(product_id)
        if not product:
            raise Http404(f"Product with id {product_id} was not found")

        form = EditProductForm(
            initial={
                "category": product["category_id"],
                "product_name": product["product_name"],
                "characteristics": product["characteristics"],
            }
        )
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Edit Product",
                "form_action": reverse("products:edit-product", args=[product_id]),
                "submit_label": "Save",
            },
        )

    def post(self, request, product_id):
        form = EditProductForm(request.POST)
        if form.is_valid():
            self.product_service.update(product_id, form.cleaned_data)
            return redirect("products:products")
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Edit Product",
                "form_action": reverse("products:edit-product", args=[product_id]),
                "submit_label": "Save",
            },
        )


class DeleteProductView(View):
    product_service = ProductService()

    def post(self, request, product_id):
        self.product_service.delete(product_id)
        return HttpResponse("")


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


class GetStoreProductsView(View):
    store_product_list_service = StoreProductListService()

    def get(self, request):
        sort_by, sort_dir = resolve_sort(
            request, STORE_PRODUCT_SORTABLE, default="products_number"
        )
        applied, where_sql, where_params = resolve_filters(request, STORE_PRODUCT_FILTERS)
        rows = self.store_product_list_service.get_all(where_sql, where_params, sort_by, sort_dir)

        return render(
            request,
            "home.html",
            {
                "list": {
                    "title": "STORE PRODUCTS",
                    "subtitle": "All products in store",
                    "rows": rows,
                    "columns": STORE_PRODUCT_COLUMNS,
                    "filters": STORE_PRODUCT_FILTERS,
                    "sort": {"by": sort_by, "dir": sort_dir},
                    "add_url": reverse("products:add-store-product"),
                    "add_label": "Add store product",
                    "empty_message": "No store products yet.",
                    "row_id_key": "UPC",
                    "actions": [
                        {
                            "label": "Edit",
                            "url_name": "products:edit-store-product",
                            "icon": "✎",
                        },
                        {
                            "label": "Delete",
                            "url_name": "products:delete-store-product",
                            "icon": "✕",
                            "method": "post",
                            "confirm": "Delete this store product?",
                        },
                    ],
                },
            },
        )


class EditStoreProductView(View):
    store_product_service = StoreProductService()

    def get(self, request, upc):
        store_product = self.store_product_service.get_by_upc(upc)
        if not store_product:
            raise Http404(f"Store product with UPC {upc} was not found")

        form = EditStoreProductForm(
            initial={
                "selling_price": store_product["selling_price"],
                "products_number": store_product["products_number"],
                "promotional_product": store_product["promotional_product"],
            }
        )
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": f"Edit Store Product: {store_product['product_name']}",
                "form_action": reverse("products:edit-store-product", args=[upc]),
                "submit_label": "Save",
            },
        )

    def post(self, request, upc):
        form = EditStoreProductForm(request.POST)
        if form.is_valid():
            self.store_product_service.update(upc, form.cleaned_data)
            return redirect("products:store-products")
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Edit Store Product",
                "form_action": reverse("products:edit-store-product", args=[upc]),
                "submit_label": "Save",
            },
        )


class DeleteStoreProductView(View):
    store_product_service = StoreProductService()

    def post(self, request, upc):
        self.store_product_service.delete(upc)
        return HttpResponse("")


class EditCategoryView(View):
    category_service = CategoryService()

    def get(self, request, category_id):
        category = self.category_service.get_by_id(category_id)
        if not category:
            raise Http404(f"Category with id {category_id} was not found")
        form = CategoryForm(initial={"category_name": category["category_name"]})
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Edit Category",
                "form_action": reverse("products:edit-category", args=[category_id]),
                "submit_label": "Save",
            },
        )

    def post(self, request, category_id):
        form = CategoryForm(request.POST)
        if form.is_valid():
            self.category_service.update(
                category_id, form.cleaned_data["category_name"]
            )
            return redirect("products:categories")
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Edit Category",
                "form_action": reverse("products:edit-category", args=[category_id]),
                "submit_label": "Save",
            },
        )
