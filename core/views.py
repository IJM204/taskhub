from .forms import ContactForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .models import Organization
from .models import Task

def organization_list(request):
    organizations = Organization.objects.all()

    return render(
        request,
        "core/organization_list.html",
        {"organizations": organizations}
    )
def home(request):
    return HttpResponse("Bienvenue sur TaskHub !")
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

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            return render(request, "core/contact_success.html")
    else:
        form = ContactForm()

    return render(request, "core/contact.html", {"form": form})
