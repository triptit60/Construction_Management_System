from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('MATERIALS', 'Materials'),
        ('LABOR', 'Labor'),
        ('PERMITS', 'Permits & Fees'),
        ('TRANSPORT', 'Transport & Freight'),
        ('MISC', 'Miscellaneous'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    date_incurred = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - ${self.amount} ({self.category})"