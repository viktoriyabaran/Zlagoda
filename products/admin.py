from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "category_number",
        "category_name",
    ]
    search_fields = [
        "category_name",
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id_product",
        "product_name",
        "category_number",
    ]
    search_fields = [
        "product_name",
    ]
    list_filter = [
        "category_number",
    ]
