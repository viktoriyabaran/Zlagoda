from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .forms import CategoryForm, ProductForm
from .services import CategoryService, ProductService


class AddCategoryView(View):
    category_service = CategoryService()

    def get(self, request):
        return render(
            request,
            "home.html",
            {
                "form": CategoryForm(),
                "form_title": "Add Category",
                "form_action": reverse("products:add-category"),
            },
        )

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            self.category_service.create(form.cleaned_data["category_name"])
            return redirect("products:categories")
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Add Category",
                "form_action": reverse("products:add-category"),
            },
        )


class GetCategoriesView(View):
    category_service = CategoryService()

    def get(self, request):
        all_categories = self.category_service.get_all()
        return render(
            request, "products/categories.html", {"categories": all_categories}
        )


class AddProductView(View):
    product_service = ProductService()

    def get(self, request):
        return render(
            request,
            "home.html",
            {
                "form": ProductForm(),
                "form_title": "Add Product",
                "form_action": reverse("products:add-product"),
            },
        )

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            self.product_service.create(form.cleaned_data)
            return redirect("core:home")
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Add Product",
                "form_action": reverse("products:add-product"),
            },
        )
