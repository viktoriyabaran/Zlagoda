from django.urls import path
from .views import AddCategoryView, GetCategoriesView

app_name = 'products'

urlpatterns = [
    path("categories/", GetCategoriesView.as_view(), name="categories"),
    path("categories/add/", AddCategoryView.as_view(), name="add-category"),
]
