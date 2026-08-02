from django import forms
from .models import InventoryItem
from django import forms
from .models import InventoryTransaction
from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        fields = [
            "item",
            "transaction_type",
            "quantity",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

class InventoryForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = [
            "name",
            "supplier",
            "project",
            "quantity",
            "unit",
            "unit_price",
            "low_stock_threshold",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "project": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "unit": forms.TextInput(attrs={"class": "form-control"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
            "low_stock_threshold": forms.NumberInput(attrs={"class": "form-control"}),
        }