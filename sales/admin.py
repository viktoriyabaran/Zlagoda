from django.contrib import admin

from .models import Check


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = [
        "card",
        "print_date",
        "sum_total",
        "vat",
    ]
