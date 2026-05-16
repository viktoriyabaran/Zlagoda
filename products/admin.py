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


@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    list_display = [
        "UPC",
        "id_product",
        "selling_price",
        "products_number",
        "promotional_product",
        "UPC_prom",
    ]
    search_fields = [
        "UPC",
        "id_product__product_name",
    ]
    list_filter = [
        "promotional_product",
    ]
