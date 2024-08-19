from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from warehouse.models import ApprovedDrug
from django.contrib.auth import get_user_model
from core.forms.approved_drug import EditApprovedDrugForm, SortingApprovedDrugForm, AddApprovedDrugForm


User = get_user_model()


@login_required
def approved_drugs_list(request):
    sorting_form = SortingApprovedDrugForm(request.GET or None)
    ad_objects = ApprovedDrug.objects.all()

    if sorting_form.is_valid():
        sort_by = sorting_form.cleaned_data.get('sort_by')
        order = sorting_form.cleaned_data.get('order')

        if sort_by:
            if order == 'desc':
                sort_by = f'-{sort_by}'
            ad_objects = ad_objects.order_by(sort_by)

    paginator = Paginator(ad_objects, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "core/approved_drugs.html", {"page_obj": page_obj,
                                                        'sorting_form': sorting_form})


@login_required
def add_approved_drug(request):
    if request.method == "POST":
        form = AddApprovedDrugForm(request.POST)
        if form.is_valid():
            approved_drug = form.save(commit=False)
            approved_drug.created_by = request.user
            approved_drug.save()
            messages.add_message(
                request, messages.SUCCESS, f"You've added a new approved drug successfully"
            )
            return redirect("approved_drugs")
    else:
        form = AddApprovedDrugForm()

    return render(request, "core/add_approved_drug.html", {"form": form})


@login_required
def edit_approved_drug(request, pk):
    approved_drug = get_object_or_404(ApprovedDrug, pk=pk)
    if request.method == "POST":
        form = EditApprovedDrugForm(request.POST, instance=approved_drug)
        if form.is_valid():
            form.created_by = request.user
            form.save()
            messages.add_message(
                request, messages.SUCCESS, f"Approved drug updated successfully"
            )
            return redirect("approved_drugs_list")
    else:
        form = EditApprovedDrugForm(instance=approved_drug)

    return render(request, "core/edit_approved_drug.html", {"form": form})


@login_required
def approved_drugs_history(request, pk):
    approved_drugs = get_object_or_404(ApprovedDrug.objects.all(), pk=pk)
    return render(
        request, "core/approved_drugs_history.html", {"approved_drugs": approved_drugs}
    )
