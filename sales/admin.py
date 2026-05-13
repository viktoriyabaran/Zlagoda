from django.contrib import admin
from .models import Check

@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = [
        "check_number",
        "id_employee",
        "card_number",
        "print_date",
        "sum_total",
        "vat",
    ]
    search_fields = [
        "check_number",
    ]
    list_filter = [
        "print_date",
    ]
