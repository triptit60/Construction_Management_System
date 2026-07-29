from django.contrib import admin
from .models import Supplier, InventoryItem

admin.site.register(Supplier)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'quantity', 'unit', 'unit_price')
    list_filter = ('supplier',)