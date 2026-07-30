from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Project,Task
from .forms import ProjectForm,TaskForm

# Create your views here.

@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save()

            messages.success(request, "Project created successfully!")
            return redirect("project_list")

        else:
         print(form.errors)
            # messages.error(request, "Please correct the errors below.")
            

    else:
         form = ProjectForm()

    return render(request, "projects/project_form.html", {
        "form": form,
    })


@login_required
def project_list(request):
    projects = Project.objects.all().order_by("-created_at")

    return render(request, "projects/project_list.html", {
        "projects": projects
    })


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    return render(request, "projects/project_detail.html", {
        "project": project
    })



@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()

            messages.success(request, "Project updated successfully!")

            return redirect("project_detail", pk=project.pk)

    else:
        form = ProjectForm(instance=project)

    return render(request, "projects/project_form.html", {
        "form": form
    })


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        project.delete()

        messages.success(request, "Project deleted successfully!")

        return redirect("project_list")

    return render(request, "projects/project_confirm_delete.html", {
        "project": project
    })


@login_required
def project_dashboard(request, pk):
    project = get_object_or_404(Project, pk=pk)  
    tasks = project.tasks.all()
    total_tasks = project.tasks.count()
    completed_tasks = project.tasks.filter(is_completed=True).count()
    pending_tasks = tasks.filter(is_completed=False).count()
    upcoming_tasks = tasks.filter(is_completed=False).order_by("due_date")[:5]

    progress = 0
    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)

    recent_tasks = tasks.order_by("-created_at")[:5]
      
    context = {
        "project": project,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "progress": progress,
        "recent_tasks": recent_tasks,
         "upcoming_tasks": upcoming_tasks,
    }

    return render(request,"projects/project_dashboard.html",context,)


@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()

            messages.success(request, "Task created successfully!")

            return redirect("task_list", project_id=project.id)

    else:
        form = TaskForm()

    return render(
        request,
        "Task/task_form.html",
        {
            "form": form,
            "project": project,
        },
    )


@login_required
def task_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    tasks = project.tasks.all().order_by("due_date")

    context = {
        "project": project,
        "tasks": tasks,
    }

    return render(
        request,
        "Task/task_list.html",
        context,
    )


@login_required
def task_detail(request, project_id, pk):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task,pk=pk,project=project,)
    context = {"project": project,"task": task,}
    return render(request,"Task/task_detail.html",context,)


@login_required
def task_update(request, project_id, pk):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task,pk=pk,project=project,)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect("task_detail",project_id=project.id, pk=task.id,)
    else:
        form = TaskForm(instance=task)
    return render( request,"Task/task_form.html",{"form": form,"project": project,"task": task,},)


@login_required
def task_delete(request, project_id, pk):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task,pk=pk, project=project,)
    if request.method == "POST":
        task.delete()

        messages.success(request, "Task deleted successfully!")

        return redirect("task_list", project_id=project.id,)

    return render( request,"Task/task_confirm_delete.html",{"project": project,"task": task,},)