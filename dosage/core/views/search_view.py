from django.shortcuts import render
from django.db import models
from warehouse.models import Storage, Product, ApprovedDrug


def search(request):
    query = request.GET.get('q')
    if query:
        storages = Storage.objects.filter(
            models.Q(rack__icontains=query) |
            models.Q(box__icontains=query) |
            models.Q(id__icontains=query)
        )
        products = Product.objects.filter(
            models.Q(serial_number__icontains=query) |
            models.Q(approved_drug__name__icontains=query) |
            models.Q(id__icontains=query)
        )
        approved_drugs = ApprovedDrug.objects.filter(
            models.Q(id__icontains=query) |
            models.Q(name__icontains=query) |
            models.Q(components__icontains=query)
        )
    else:
        storages = Storage.objects.none()
        products = Product.objects.none()
        approved_drugs = ApprovedDrug.objects.none()

    context = {
        'storages': storages,
        'products': products,
        'approved_drugs': approved_drugs,
        'query': query,
    }
    return render(request, 'core/search_result.html', context)
