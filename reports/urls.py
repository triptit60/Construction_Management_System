from django.urls import path
from . import views

app_name = "reports"  

urlpatterns = [
            path("", views.reports_dashboard, name="reports_dashboard"),
            path('inventory/', views.inventory_report, name='inventory_report'),
            path('expense/',views.expense_report,name='expense_report'),
            path('projects/', views.project_report,name='project_report'),

            #for excel
            path("projects/export/excel/",views.export_project_excel,name="export_project_excel",),
            path("expenses/export/excel/",views.export_expense_excel,name="export_expense_excel",),
            path("inventory/export/excel/",views.export_inventory_excel,name="export_inventory_excel",),

            #for pdf
            path("projects/export/pdf/",views.export_project_pdf,name="export_project_pdf",),
            path("expenses/export/pdf/",views.export_expense_pdf, name="export_expense_pdf",),
            path("inventory/export/pdf/",views.export_inventory_pdf, name="export_inventory_pdf",),
]
