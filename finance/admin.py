from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('project', 'category', 'amount', 'date_incurred', 'logged_by')
    list_filter = ('category', 'project')
