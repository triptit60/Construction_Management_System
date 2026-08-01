from django.contrib import admin
from .models import Supplier, InventoryItem,InventoryTransaction

admin.site.register(Supplier)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'quantity', 'unit', 'unit_price')
    list_filter = ('supplier',)

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "transaction_type",
        "quantity",
        "created_at",
    )
    list_filter = (
        "transaction_type",
        "created_at",
    )
    search_fields = (
        "item__name",
    )