from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from warehouse.models import Storage, Product, ApprovedDrug
from django.contrib.auth import get_user_model


User = get_user_model()


@login_required
def view_storage_products(request, pk):
    storage = get_object_or_404(Storage, pk=pk)
    products = Product.objects.filter(storage=storage)
    paginator = Paginator(products, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "core/storage_products.html",
        {"storage": storage, "products": products, "page_obj": page_obj},
    )


@login_required
def view_approved_drug_products(request, pk):
    approved_drug = get_object_or_404(ApprovedDrug, pk=pk)
    products = Product.objects.filter(storage=ApprovedDrug)
    paginator = Paginator(products, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "core/storage_products.html",
        {"approved_drug": approved_drug, "products": products, "page_obj": page_obj},
    )


@login_required
def products_by_approved_drug(request, pk):
    approved_drug = ApprovedDrug.objects.get(pk=pk)
    products = Product.objects.filter(approved_drug=approved_drug)
    paginator = Paginator(products, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "core/products_by_approved_drug.html",
        {"approved_drug": approved_drug, "products": products, "page_obj": page_obj},
    )


@login_required
def approved_drug_by_name(request, name):
    approved_drug = ApprovedDrug.objects.filter(name=name)
    paginator = Paginator(approved_drug, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "core/approved_drug_by_name.html",
        {"approved_drug": approved_drug, "page_obj": page_obj},
    )
