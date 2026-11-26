from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .models import Organization


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