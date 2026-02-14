from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),
    path('', include('core.urls')),
    path('employees/', include('employees.urls')),
    path('products/', include('products.urls')),
    path('sales/', include('sales.urls')),
    path('customers/', include('customers.urls')),
]
