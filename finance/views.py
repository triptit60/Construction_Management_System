from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ExpenseForm
from .models import Expense
from projects.models import Project
from django.shortcuts import get_object_or_404

from django.db.models import Sum, Avg, Max
from django.utils import timezone
# Create your views here.

@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.logged_by = request.user
            expense.save()

            messages.success(request, "Expense added successfully!")
            return redirect("expense_list")
    else:
        form = ExpenseForm()
    return render(request, "finance/expense_form.html", {"form": form})


@login_required
def expense_list(request):
    expenses = Expense.objects.select_related(
        "project", "logged_by"
    ).order_by("-date_incurred", "-created_at")

    projects = Project.objects.all()

    # Get filter values
    project = request.GET.get("project")
    category = request.GET.get("category")
    date = request.GET.get("date")

    # Apply filters
    if project:
        expenses = expenses.filter(project_id=project)
    if category:
        expenses = expenses.filter(category=category)
    if date:
        expenses = expenses.filter(date_incurred=date)
    context = {
        "expenses": expenses,
        "projects": projects,
        "categories": Expense.CATEGORY_CHOICES,
    }
    return render(request, "finance/expense_list.html", context)


@login_required
def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    return render(request, "finance/expense_detail.html", {"expense": expense})



@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            updated_expense = form.save(commit=False)
            updated_expense.logged_by = request.user
            updated_expense.save()
            messages.success(request, "Expense updated successfully!")
            return redirect("expense_detail", pk=expense.pk)
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "finance/expense_form.html", {"form": form})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted successfully!")
        return redirect("expense_list")
    return render(request, "finance/expense_confirm_delete.html", {"expense": expense})



@login_required
def finance_dashboard(request):

    total_expenses = Expense.objects.aggregate(total=Sum("amount"))["total"] or 0
    monthly_expenses = Expense.objects.filter(
        date_incurred__month=timezone.now().month,
        date_incurred__year=timezone.now().year,).aggregate(total=Sum("amount"))["total"] or 0
    average_expense = Expense.objects.aggregate(avg=Avg("amount"))["avg"] or 0
    highest_expense = Expense.objects.aggregate(highest=Max("amount"))["highest"] or 0
    recent_expenses = Expense.objects.select_related("project","logged_by").order_by("-created_at")[:5]
    project_expense_summary = (Expense.objects.values("project__id", "project__name").annotate(total=Sum("amount")).order_by("-total"))
    expense_category_chart = (Expense.objects.values("category").annotate(total=Sum("amount")).order_by("category"))

    context = {
        "total_expenses": total_expenses,
        "monthly_expenses": monthly_expenses,
        "average_expense": average_expense,
        "highest_expense": highest_expense,
        "recent_expenses": recent_expenses,
        "project_expense_summary": project_expense_summary,
         "expense_category_chart": list(expense_category_chart),
    }
    return render(request,"finance/dashboard.html",context,)