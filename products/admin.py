from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "category_number",
        "category_name",
    ]
    search_fields = [
        "category_name",
    ]
