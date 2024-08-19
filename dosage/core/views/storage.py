from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from warehouse.models import Storage
from core.forms.storage import EditStorageForm, SortingStorageForm, AddStorageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


User = get_user_model()


@login_required
def storage_list(request):
    storage_objects = Storage.objects.all()
    sorting_form = SortingStorageForm(request.GET or None)

    if sorting_form.is_valid():
        sort_by = sorting_form.cleaned_data.get('sort_by')
        order = sorting_form.cleaned_data.get('order')

        if sort_by:
            if order == 'desc':
                sort_by = f'-{sort_by}'
            ad_objects = storage_objects.order_by(sort_by)


    paginator = Paginator(storage_objects, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "core/storage_list.html", {"page_obj": page_obj, 'sorting_form': sorting_form})


@login_required
def add_storage(request):
    if request.method == "POST":
        form = AddStorageForm(request.POST)
        if form.is_valid():
            storage = form.save(commit=False)
            storage.created_by = request.user
            storage.save()
            messages.add_message(
                request, messages.SUCCESS, f"You've added a new storage successfully"
            )
            return redirect("storage_list")
    else:
        form = AddStorageForm()

    return render(request, "core/add_storage.html", {"form": form})


@login_required
def edit_storage(request, pk):
    storage = get_object_or_404(Storage, pk=pk)
    if request.method == "POST":
        form = EditStorageForm(request.POST, instance=storage)
        if form.is_valid():
            form.created_by = request.user
            form.save()
            messages.add_message(
                request, messages.SUCCESS, f"Storage updated successfully"
            )
            return redirect("storage_list")
    else:
        form = EditStorageForm(instance=storage)

    return render(request, "core/edit_storage.html", {"form": form})


@login_required
def storage_history(request, pk):
    storage = get_object_or_404(Storage.objects.all(), pk=pk)

    return render(request, "core/storage_history.html", {"storage": storage})
