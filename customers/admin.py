from django.contrib import admin
from .models import CustomerCard

@admin.register(CustomerCard)
class CustomerCardAdmin(admin.ModelAdmin):
    list_display = [
        "card_number",
        "cust_surname",
        "cust_name",
        "phone_number",
        "percent",
    ]
    search_fields = [
        "card_number",
        "cust_surname",
        "phone_number",
    ]
    list_filter = [
        "percent",
    ]
