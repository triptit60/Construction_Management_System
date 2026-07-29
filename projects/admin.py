from django.contrib import admin
from .models import Project, Task, Activity

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'status', 'start_date')
    list_filter = ('status',)
    search_fields = ('name', 'location')




@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "action_type", "message", "created_at")
    list_filter = ("action_type", "created_at")
    search_fields = ("message", "user__username")
    ordering = ("-created_at",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "assigned_to", "is_completed", "due_date")
    list_filter = ("is_completed",)