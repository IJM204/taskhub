from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path(
    "organizations/",
    views.organization_list,
    name="organization_list"),
]
