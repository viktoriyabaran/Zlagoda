from django.urls import path

from .views import (
    AddCategoryView,
    AddProductView,
    EditProductView,
    AddStoreProductView,
    GetCategoriesView,
    GetProductsView,
    GetStoreProductsView,
)

app_name = "products"

urlpatterns = [
    path("categories/", GetCategoriesView.as_view(), name="categories"),
    path("categories/add/", AddCategoryView.as_view(), name="add-category"),
    path("products/add/", AddProductView.as_view(), name="add-product"),
    path(
        "store-products/add/", AddStoreProductView.as_view(), name="add-store-product"
    ),
    path("store-products/", GetStoreProductsView.as_view(), name="store-products"),
    path("", GetProductsView.as_view(), name="products"),
    path("products/<int:product_id>/edit/", EditProductView.as_view(), name="edit-product"),
]
