from django.contrib import admin
from .models import Check

@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "employee",
        "card",
        "print_date",
        "sum_total",
        "vat",
    ]
    search_fields = [
        "id",
    ]
    list_filter = [
        "print_date",
    ]
