from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import InventoryForm
from .models import InventoryItem
# Create your views here.


@login_required
def inventory_list(request):
    items = InventoryItem.objects.all().order_by("-created_at")
    return render(request, "inventory/inventory_list.html", {"items": items})


@login_required
def inventory_create(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Inventory item added successfully.")
            return redirect("inventory_list")

    else:
        form = InventoryForm()
    return render(request, "inventory/inventory_form.html", {"form": form})


@login_required
def inventory_detail(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    return render(request, "inventory/inventory_detail.html", {
        "item": item
    })


@login_required
def inventory_update(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == "POST":
        form = InventoryForm(request.POST, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, "Inventory updated successfully.")
            return redirect("inventory_detail", pk=item.pk)

    else:
        form = InventoryForm(instance=item)
    return render(request,"inventory/inventory_form.html", {"form": form})


@login_required
def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Inventory item deleted successfully.")
        return redirect("inventory_list")

    return render(request,"inventory/inventory_confirm_delete.html", {"item": item})