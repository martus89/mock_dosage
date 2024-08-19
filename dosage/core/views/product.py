from django.core.paginator import Paginator
from warehouse.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from core.forms.product import EditProductForm, SortingProductForm, AddProductForm
from django.contrib import messages


User = get_user_model()


@login_required
def product_list(request):
    product_objects = Product.objects.all()
    sorting_form = SortingProductForm(request.GET or None)

    if sorting_form.is_valid():
        sort_by = sorting_form.cleaned_data.get('sort_by')
        order = sorting_form.cleaned_data.get('order')

        if sort_by:
            if order == 'desc':
                sort_by = f'-{sort_by}'
            product_objects = product_objects.order_by(sort_by)

    paginator = Paginator(product_objects, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "core/products.html", {"page_obj": page_obj, 'sorting_form': sorting_form})


@login_required
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.add_message(
                request, messages.SUCCESS, f"You've added a new product successfully"
            )
            return redirect("product_list")
    else:
        form = AddProductForm()

    return render(request, "core/add_product.html", {"form": form})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = EditProductForm(request.POST, instance=product)
        if form.is_valid():
            form.created_by = request.user
            form.save()
            messages.add_message(
                request, messages.SUCCESS, f"Product updated successfully"
            )
            return redirect("product_list")
    else:
        form = EditProductForm(instance=product)

    return render(request, "core/edit_product.html", {"form": form})


@login_required
def product_history(request, pk):
    products = get_object_or_404(Product.objects.all(), pk=pk)

    return render(request, "core/products_history.html", {"products": products})
