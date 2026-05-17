from django.shortcuts import redirect, render
from django.views import View
from .forms import CategoryForm
from .services import CategoryService

class AddCategoryView(View):
    category_service = CategoryService()

    def get(self, request):
        form = CategoryForm()
        return render(request, "products/add-category.html", {"form": form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            self.category_service.create(form.cleaned_data["category_name"])
            return redirect("products:categories")
        return render(request, "products/add-category.html", {"form": form})

class GetCategoriesView(View):
    category_service = CategoryService()

    def get(self, request):
        all_categories = self.category_service.get_all()
        return render(request, "products/categories.html", {"categories": all_categories})
