from django.urls import path
from .views import AddCategoryView, categories

app_name = 'products'

urlpatterns = [
    path("categories/", categories, name="categories"),
    path("categories/add/", AddCategoryView.as_view(), name="add-category"),
]
