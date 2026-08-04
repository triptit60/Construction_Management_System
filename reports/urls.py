from django.urls import path
from . import views

app_name = "reports"  

urlpatterns = [
            path("", views.reports_dashboard, name="reports_dashboard"),
            path('inventory/', views.inventory_report, name='inventory_report'),
            path('expense/',views.expense_report,name='expense_report'),
            path('projects/', views.project_report,name='project_report'),
]