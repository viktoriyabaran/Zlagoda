from django.contrib import admin
from .models import CustomerCard

@admin.register(CustomerCard)
class CustomerCardAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "cust_surname",
        "cust_name",
        "phone_number",
        "percent",
    ]
    search_fields = [
        "cust_surname",
        "phone_number",
    ]
    list_filter = [
        "percent",
    ]
