from django.urls import path

from .views import (
    AddCategoryView,
    AddProductView,
    AddStoreProductView,
    DeleteCategoryView,
    DeleteProductView,
    DeleteStoreProductView,
    EditCategoryView,
    EditProductView,
    EditStoreProductView,
    GetCategoriesView,
    GetProductsView,
    GetStoreProductsView,
    ProductDetailView,
)

app_name = "products"

urlpatterns = [
    path("categories/", GetCategoriesView.as_view(), name="categories"),
    path("categories/add/", AddCategoryView.as_view(), name="add-category"),
    path(
        "categories/<int:category_id>/edit/",
        EditCategoryView.as_view(),
        name="edit-category",
    ),
    path(
        "categories/<int:category_id>/delete/",
        DeleteCategoryView.as_view(),
        name="delete-category",
    ),
    path("products/add/", AddProductView.as_view(), name="add-product"),
    path(
        "store-products/add/", AddStoreProductView.as_view(), name="add-store-product"
    ),
    path("store-products/", GetStoreProductsView.as_view(), name="store-products"),
    path("", GetProductsView.as_view(), name="products"),
    path(
        "products/<int:product_id>/edit/",
        EditProductView.as_view(),
        name="edit-product",
    ),
    path(
        "store-products/<str:upc>/edit/",
        EditStoreProductView.as_view(),
        name="edit-store-product",
    ),
    path(
        "products/<int:product_id>/delete/",
        DeleteProductView.as_view(),
        name="delete-product",
    ),
    path(
        "store-products/<str:upc>/delete/",
        DeleteStoreProductView.as_view(),
        name="delete-store-product",
    ),
    path(
        "products/<int:product_id>/", ProductDetailView.as_view(), name="product-detail"
    ),
]
