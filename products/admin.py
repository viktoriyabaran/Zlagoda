from django.contrib import admin

from .models import Category, Product, StoreProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "category_name",
    ]
    search_fields = [
        "category_name",
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product_name",
        "category",
    ]
    search_fields = [
        "product_name",
    ]
    list_filter = [
        "category",
    ]


@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    list_display = [
        "UPC",
        "product",
        "selling_price",
        "products_number",
        "promotional_product",
        "UPC_prom",
    ]
    search_fields = [
        "UPC",
        "product__product_name",
    ]
    list_filter = [
        "promotional_product",
    ]
