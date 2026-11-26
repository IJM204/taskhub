from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView

from .models import Organization, Task, Project
from .forms import ContactForm, ProjectForm


def home(request):
    return HttpResponse("Bienvenue sur TaskHub !")


def organization_list(request):
    organizations = Organization.objects.all()

    return render(
        request,
        "core/organization_list.html",
        {"organizations": organizations}
    )


def organization_detail(request, slug):
    organization = get_object_or_404(
        Organization,
        slug=slug
    )

    return render(
        request,
        "core/organization_detail.html",
        {"organization": organization}
    )


def task_list(request):
    tasks = Task.objects.select_related(
        "project",
        "project__organization"
    ).all()

    return render(
        request,
        "core/task_list.html",
        {"tasks": tasks}
    )


# EXERCICE 27 : FORMULAIRE DE CONTACT

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            return render(
                request,
                "core/contact_success.html"
            )
    else:
        form = ContactForm()

    return render(
        request,
        "core/contact.html",
        {"form": form}
    )


# EXERCICE 28 : CREATION D'UN PROJET

def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save()

            messages.success(
                request,
                "Projet créé avec succès."
            )

            return redirect(
                "core:organization_detail",
                slug=project.organization.slug
            )
    else:
        form = ProjectForm()

    return render(
        request,
        "core/project_form.html",
        {"form": form}
    )


# EXERCICE 29 : MODIFICATION D'UN PROJET

def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        form = ProjectForm(
            request.POST,
            instance=project
        )

        if form.is_valid():
            project = form.save()

            messages.success(
                request,
                "Projet modifié avec succès."
            )

            return redirect(
                "core:organization_detail",
                slug=project.organization.slug
            )
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "core/project_form.html",
        {
            "form": form,
            "project": project
        }
    )


# EXERCICE 30 : SUPPRESSION D'UN PROJET

def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        organization_slug = project.organization.slug

        project.delete()

        messages.success(
            request,
            "Projet supprimé avec succès."
        )

        return redirect(
            "core:organization_detail",
            slug=organization_slug
        )

    return render(
        request,
        "core/project_confirm_delete.html",
        {"project": project}
    )


# EXERCICE 32 : LISTVIEW ET DETAILVIEW

class ProjectListView(ListView):
    model = Project
    template_name = "core/project_list.html"
    context_object_name = "projects"
    ordering = ["id"]


class ProjectDetailView(DetailView):
    model = Project
    template_name = "core/project_detail.html"
    context_object_name = "project"