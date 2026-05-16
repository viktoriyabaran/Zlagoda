from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .forms import UserAdminForm
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ["username", "employee__empl_surname", "employee__empl_name"]
    search_fields = ["username", "employee__empl_surname", "employee__empl_name"]

    def save_model(self, request, obj, form, change):
        new_password = form.cleaned_data.get("password")
        if new_password:
            obj.password = make_password(new_password)
        elif change:
            obj.password = type(obj).objects.get(pk=obj.pk).password
        super().save_model(request, obj, form, change)
