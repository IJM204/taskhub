from django.http import HttpResponse

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
