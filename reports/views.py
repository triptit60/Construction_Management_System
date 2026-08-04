from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.db.models import Sum

from projects.models import Project
from inventory.models import InventoryItem
from finance.models import Expense


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
    context = { 'inventory': inventory,}
    return render(request, 'reports/inventory_report.html', context)



def expense_report(request):
    expenses = Expense.objects.select_related('project','logged_by').order_by('-date_incurred')
    context = {'expenses': expenses,}
    return render(request, 'reports/expense_report.html', context)


def project_report(request):
    projects = Project.objects.select_related('manager','created_by').all()
    context = {'projects': projects,}
    return render(request, 'reports/project_report.html', context)

