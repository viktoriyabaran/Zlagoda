from django.shortcuts import render


# Define core views (login, logout, dashboard) here
def home(request):
    return render(request, "home.html")
