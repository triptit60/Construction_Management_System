from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Project
from .forms import ProjectForm

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