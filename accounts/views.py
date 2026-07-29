from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import UserProfile
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from projects.models import Activity

from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render

from projects.models import Project, Task
from inventory.models import InventoryItem
from finance.models import Expense


@login_required
def dashboard(request):

    # ----------------------------
    # Project Statistics
    # ----------------------------

    total_projects = Project.objects.count()

    planning_projects = Project.objects.filter(
        status="PLANNING"
    ).count()

    active_projects = Project.objects.filter(
        status="IN_PROGRESS"
    ).count()

    completed_projects = Project.objects.filter(
        status="COMPLETED"
    ).count()

    on_hold_projects = Project.objects.filter(
        status="ON_HOLD"
    ).count()

    # ----------------------------
    # Inventory Statistics
    # ----------------------------

    total_items = InventoryItem.objects.count()

    total_stock = InventoryItem.objects.aggregate(
        total=Sum("quantity")
    )["total"] or 0

    low_stock_items = InventoryItem.objects.filter(
        quantity__lt=20
    )

    # ----------------------------
    # Expense Statistics
    # ----------------------------

    total_expenses = Expense.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    monthly_expenses = Expense.objects.filter(
        date_incurred__month=date.today().month,
        date_incurred__year=date.today().year,
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    # ----------------------------
    # Task Statistics
    # ----------------------------

    total_tasks = Task.objects.count()

    completed_tasks = Task.objects.filter(
        is_completed=True
    ).count()

    pending_tasks = Task.objects.filter(
        is_completed=False
    ).count()

    upcoming_tasks = Task.objects.filter(
        is_completed=False,
        due_date__gte=date.today()
    ).order_by("due_date")[:5]

    # ----------------------------
    # Recent Projects
    # ----------------------------

    recent_projects = Project.objects.select_related(
        "manager"
    ).order_by("-created_at")[:5]


    # ===========================
    # Recent Activities
    # ===========================

    recent_activities = Activity.objects.select_related(
        "user"
    ).order_by("-created_at")[:8]

    # ----------------------------
    # Recent Expenses
    # ----------------------------

    recent_expenses = Expense.objects.select_related(
        "project",
        "logged_by"
    ).order_by("-created_at")[:5]

    # ----------------------------
    # Chart Data
    # ----------------------------

    project_status_chart = Project.objects.values(
        "status"
    ).annotate(
        total=Count("id")
    )

    expense_chart = Expense.objects.values(
        "category"
    ).annotate(
        total=Sum("amount")
    )

    # ----------------------------
    # Context
    # ----------------------------

    context = {

        "total_projects": total_projects,
        "planning_projects": planning_projects,
        "active_projects": active_projects,
        "completed_projects": completed_projects,
        "on_hold_projects": on_hold_projects,

        "total_items": total_items,
        "total_stock": total_stock,
        "low_stock_items": low_stock_items,

        "total_expenses": total_expenses,
        "monthly_expenses": monthly_expenses,

        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,

        "recent_projects": recent_projects,
        "recent_expenses": recent_expenses,
        "upcoming_tasks": upcoming_tasks,
        "recent_activities": recent_activities,

        "project_status_chart": list(project_status_chart),
        "expense_chart": list(expense_chart),

    }

    return render(
        request,
        "accounts/dashboard.html",
        context,
    )


# for registrartion
def register(request):
    # If the user submits the registration form
    if request.method == "POST":
        # Populate the form with submitted data
        form = SignUpForm(request.POST)

        # Check if all form data is valid
        if form.is_valid():

            # Save the User object but don't commit if you want to modify it first
            user = form.save(commit=False)

            # Save the User to the database
            user.save()

            # Create the corresponding UserProfile
            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data["role"]
            )

            # Redirect the user to the login page
            return redirect("login")

    else:
        # If it's a GET request, display an empty form
        form = SignUpForm()

    # Render the registration page with the form
    return render(request, "registration/register.html", {"form": form})

class UserLoginView(LoginView):
    template_name = "registration/login.html"

def logout_user(request):
    logout(request)
    messages.success(request,("You have been looged out...."))
    return redirect ('login')