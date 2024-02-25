from django.shortcuts import render
from django.http import HttpResponse


def homepage(request):
    return render(request, 'warehouse/index.html')


def login_page(request):
    return render(request, 'warehouse/login.html')


def register(request):
    return render(request, 'warehouse/register.html')


def users_view(request):
    return render(request, 'warehouse/users.html')


def storage_view(request):
    return render(request, 'warehouse/storage.html')


def approved_drugs_view(request):
    return render(request, 'warehouse/approved_drugs.html')


def product_view(request):
    return render(request, 'warehouse/products.html')
