from django.db import models
from projects.models import Project

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    name = models.CharField(max_length=200)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='items')
    quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=50, help_text="e.g., bags, tons, units")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="inventory_items",null=True,blank=True)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def total_value(self):
        return self.quantity * self.unit_price

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold

    def __str__(self):
        return self.name

#For inventory Transcation
class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
    ]
    item = models.ForeignKey(InventoryItem,on_delete=models.CASCADE,related_name="transactions")
    transaction_type = models.CharField(max_length=3,choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - {self.transaction_type} ({self.quantity})"