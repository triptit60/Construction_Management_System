from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.models import User

from projects.models import Project
from inventory.models import InventoryItem
from finance.models import Expense
from inventory.models import Supplier
from django.db.models import F
from django.db import models


def reports_dashboard(request):
    total_projects = Project.objects.count()
    total_inventory = InventoryItem.objects.count()
    total_inventory_value = sum(item.total_value for item in InventoryItem.objects.all())
    total_expenses = ( Expense.objects.aggregate(total=Sum("amount"))["total"] or 0)
    low_stock = sum(1 for item in InventoryItem.objects.all()if item.is_low_stock)
    context = {
        "total_projects": total_projects,
        "total_inventory": total_inventory,
        "total_inventory_value": total_inventory_value,
        "total_expenses": total_expenses,
        "low_stock": low_stock,
    }
    return render(request, "reports/dashboard.html", context)


def inventory_report(request):
    inventory = InventoryItem.objects.select_related('supplier', 'project')

            # Get filter values
    project = request.GET.get('project')
    supplier = request.GET.get('supplier')
    search = request.GET.get('search')
    low_stock = request.GET.get('low_stock')

    # Apply filters
    if project:
        inventory = inventory.filter(project_id=project)

    if supplier:
        inventory = inventory.filter(supplier_id=supplier)

    if search:
        inventory = inventory.filter(name__icontains=search)

    if low_stock:
        inventory = inventory.filter(
            quantity__lte=models.F('low_stock_threshold')
        )

    context = { 'inventory': inventory, 'projects': Project.objects.all(),'suppliers': Supplier.objects.all(),}
    return render(request, 'reports/inventory_report.html', context)



def expense_report(request):
    expenses = Expense.objects.select_related('project','logged_by').order_by('-date_incurred')

             
    # Get filter values
    project = request.GET.get('project')
    category = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    # Apply filters
    if project:
        expenses = expenses.filter(project_id=project)

    if category:
        expenses = expenses.filter(category=category)

    if date_from:
        expenses = expenses.filter(date_incurred__gte=date_from)

    if date_to:
        expenses = expenses.filter(date_incurred__lte=date_to)


    context = {'expenses': expenses,'projects': Project.objects.all(),
        'categories': Expense.CATEGORY_CHOICES,}
    return render(request, 'reports/expense_report.html', context)



def project_report(request):
    projects = Project.objects.select_related('manager','created_by').all()

          # Get filter values
    status = request.GET.get('status')
    manager = request.GET.get('manager')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Apply filters
    if status:
        projects = projects.filter(status=status)

    if manager:
        projects = projects.filter(manager_id=manager)

    if start_date:
        projects = projects.filter(start_date__gte=start_date)

    if end_date:
        projects = projects.filter(end_date__lte=end_date)


    context = {'projects': projects,'managers': User.objects.all(),
        'statuses': Project.STATUS_CHOICES,}
    return render(request, 'reports/project_report.html', context)

