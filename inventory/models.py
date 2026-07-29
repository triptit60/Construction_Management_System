from django.db import models

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

    def __str__(self):
        return self.name
