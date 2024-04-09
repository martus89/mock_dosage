from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def storage_view(request):
    pass


@login_required
def approved_drugs_view(request):
    pass


@login_required
def product_view(request):
    pass


@login_required
def users_view(request):
    pass
