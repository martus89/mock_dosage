from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from warehouse.models import Storage, Product, ApprovedDrug


def homepage(request):
    context = {}
    return render(request, 'core/homepage.html', context)


@login_required
def storage_view(request):
    context = {}
    return render(request, 'core/storage_list.html', context)


@login_required
def approved_drugs_view(request):
    context = {}
    return render(request, 'core/approved_drugs.html', context)


@login_required
def product_view(request):
    context = {}
    return render(request, 'core/products.html', context)


@login_required
def users_view(request):
    context = {}
    return render(request, 'core/users.html', context)


@login_required()
def storage_list(request):
    storage_objects = Storage.objects.all()
    paginator = Paginator(storage_objects, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/storage_list.html', {'page_obj': page_obj})


@login_required()
def storage_history(request, pk):
    storage = get_object_or_404(Storage, pk=pk)
    return render(request, 'core/storage_history.html', {'storage': storage})


@login_required()
def view_storage_products(request, pk):
    storage = get_object_or_404(Storage, pk=pk)
    products = Product.objects.filter(storage=storage)
    paginator = Paginator(products, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/storage_products.html', {'storage': storage, 'products': products, 'page_obj': page_obj})


@login_required()
def product_list(request):
    product_objects = Product.objects.all()
    paginator = Paginator(product_objects, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/products.html', {'page_obj': page_obj})


@login_required()
def product_history(request, pk):
    products = get_object_or_404(Product, pk=pk)
    return render(request, 'core/products_history.html', {'products': products})


@login_required()
def approved_drugs_list(request):
    ad_objects = ApprovedDrug.objects.all()
    paginator = Paginator(ad_objects, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/approved_drugs.html', {'page_obj': page_obj})


@login_required()
def approved_drugs_history(request, pk):
    approved_drugs = get_object_or_404(ApprovedDrug, pk=pk)
    return render(request, 'core/approved_drugs_history.html', {'approved_drugs': approved_drugs})


@login_required()
def view_approved_drug_products(request, pk):
    approved_drug = get_object_or_404(ApprovedDrug, pk=pk)
    products = Product.objects.filter(storage=ApprovedDrug)
    paginator = Paginator(products, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/storage_products.html', {'approved_drug': approved_drug, 'products': products, 'page_obj': page_obj})


@login_required()
def products_by_approved_drug(request, pk):
    approved_drug = ApprovedDrug.objects.get(pk=pk)
    products = Product.objects.filter(approved_drug=approved_drug)
    return render(request, 'core/products_by_approved_drug.html', {'approved_drug': approved_drug, 'products': products})