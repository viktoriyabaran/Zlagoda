from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        # "employee__full_name"
        # "employee__role"
    ]
    search_fields = [
        "username",
        # "employee__full_name"
        # "employee__role"
    ]
    list_filter = [
        # "employee__full_name"
    ]
