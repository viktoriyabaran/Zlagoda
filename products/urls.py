from django.urls import path

from .views import (
    AddCategoryView,
    AddProductView,
    AddStoreProductView,
    GetCategoriesView,
)

app_name = "products"

urlpatterns = [
    path("categories/", GetCategoriesView.as_view(), name="categories"),
    path("categories/add/", AddCategoryView.as_view(), name="add-category"),
    path("products/add/", AddProductView.as_view(), name="add-product"),
    path("store-products/add/", AddStoreProductView.as_view(), name="add-store-product"),
]
