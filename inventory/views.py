from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render, redirect
from .forms import InventoryTransactionForm

from .forms import InventoryForm,SupplierForm
from .models import InventoryItem,InventoryTransaction,Supplier
from django.db.models import F
# Create your views here.

from accounts.decorators import role_required


@login_required
@role_required([
    'ADMIN',
    'PROJECT_MANAGER',
    'SITE_ENGINEER',
    'ACCOUNTANT'
])
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier/supplier_list.html', {'suppliers': suppliers})


@login_required
@role_required([
    'ADMIN',
    'SITE_ENGINEER'
])
def supplier_create(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'supplier/supplier_form.html', { 'form': form})



@login_required
@role_required([
    'ADMIN',
    'PROJECT_MANAGER',
    'SITE_ENGINEER',
    'ACCOUNTANT'
])
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    inventory_items = InventoryItem.objects.filter(supplier=supplier)
    return render(request, 'supplier/supplier_detail.html', { 'supplier': supplier, 'inventory_items': inventory_items })


@login_required
@role_required([
    'ADMIN',
    'SITE_ENGINEER'
])
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_detail', pk=pk)
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'supplier/supplier_form.html', {'form': form})



@login_required
@role_required([
    'ADMIN',
    'SITE_ENGINEER'
])
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == "POST":
        supplier.delete()
        return redirect('supplier_list')

    return render(request, 'supplier/supplier_confirm_delete.html', {'supplier': supplier})



@login_required
@role_required([
    'ADMIN',
    'PROJECT_MANAGER',
    'SITE_ENGINEER',
    'ACCOUNTANT'
])
def inventory_detail(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    transactions = (InventoryTransaction.objects.filter(item=item).order_by("-created_at"))
    context = {"item": item,"transactions": transactions,}
    return render(request, "inventory/inventory_detail.html", context)


@login_required
@role_required([
    'ADMIN',
    'SITE_ENGINEER'
])
def transaction_create(request):
    if request.method == "POST":
        form = InventoryTransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            item = transaction.item

            # Stock In
            if transaction.transaction_type == "IN":
                item.quantity += transaction.quantity

            # Stock Out
            elif transaction.transaction_type == "OUT":
                if item.quantity < transaction.quantity:
                    messages.error(request, "Not enough stock available.")
                    return render(request, "inventory/transaction_form.html", {"form": form})

                item.quantity -= transaction.quantity

            # Save updated quantity
            item.save()

            # Save transaction
            transaction.save()
            messages.success(request, "Inventory transaction recorded successfully!")
            return redirect("inventory_list")

    else:
        form = InventoryTransactionForm()
    return render(request, "inventory/transaction_form.html", {"form": form})


@login_required
@role_required([
    'ADMIN',
    'PROJECT_MANAGER',
    'SITE_ENGINEER',
    'ACCOUNTANT'
])
def transaction_list(request):
    transactions = InventoryTransaction.objects.select_related("item").order_by("-created_at")

    return render(request, "inventory/transaction_list.html", {
        "transactions": transactions,})



@login_required
@role_required([
    'ADMIN',
    'PROJECT_MANAGER',
    'SITE_ENGINEER',
    'ACCOUNTANT'
])
def inventory_dashboard(request):
    items = InventoryItem.objects.all()

    total_materials = items.count()

    low_stock_items = items.filter(
        quantity__lte=F("low_stock_threshold")
    )

    total_inventory_value = sum(
        item.total_value() for item in items
    )

    recent_items = items.order_by("-created_at")[:5]

    context = {
        "total_materials": total_materials,
        "low_stock_count": low_stock_items.count(),
        "low_stock_items": low_stock_items,
        "recent_items": recent_items,
        "total_inventory_value": total_inventory_value,
    }
    return render( request,"inventory/inventory_dashboard.html",context,)



@login_required
@role_required([
    'ADMIN',
    'PROJECT_MANAGER',
    'SITE_ENGINEER',
    'ACCOUNTANT'
])
def inventory_list(request):
    items = InventoryItem.objects.all().order_by("-created_at")
    total_materials = items.count()
    low_stock_count = items.filter(quantity__lte=F("low_stock_threshold")).count()
    total_inventory_value = sum(item.total_value() for item in items)
    context = {
        "items": items,
        "total_materials": total_materials,
        "low_stock_count": low_stock_count,
        "total_inventory_value": total_inventory_value,
    }
    return render(request, "inventory/inventory_list.html", context)


@login_required
@role_required([
    'ADMIN',
    'SITE_ENGINEER'
])
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
@role_required([
    'ADMIN',
    'PROJECT_MANAGER',
    'SITE_ENGINEER',
    'ACCOUNTANT'
])
def inventory_detail(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    return render(request, "inventory/inventory_detail.html", {
        "item": item
    })


@login_required
@role_required([
    'ADMIN',
    'SITE_ENGINEER'
])
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
@role_required([
    'ADMIN',
    'SITE_ENGINEER'
])
def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Inventory item deleted successfully.")
        return redirect("inventory_list")

    return render(request,"inventory/inventory_confirm_delete.html", {"item": item})


    