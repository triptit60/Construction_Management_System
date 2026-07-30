
from django.utils import timezone
timezone.now
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    STATUS_CHOICES = [
        ('PLANNING', 'Planning'),
        ('IN_PROGRESS', 'In Progress'),
        ('ON_HOLD', 'On Hold'),
        ('COMPLETED', 'Completed'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_projects')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNING')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_projects')
    project_code = models.CharField(max_length=20,unique=True,default="Pending Code")
    client = models.CharField(max_length=200, null=True, blank=True,default="Pending Client")
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="tasks")
    title = models.CharField(max_length=200,)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES,default="MEDIUM")
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




class Activity(models.Model):
    ACTION_CHOICES = [
        ("PROJECT", "Project"),
        ("TASK", "Task"),
        ("INVENTORY", "Inventory"),
        ("EXPENSE", "Expense"),
        ("USER", "User"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.message