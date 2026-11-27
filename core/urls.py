from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path(
    "organizations/",
    views.organization_list,
    name="organization_list"),
    path(
    "organizations/<slug:slug>/",
    views.organization_detail,
    name="organization_detail"
    ),
    path("tasks/",views.TaskListView.as_view(),name="task_list"),
    path("contact/", views.contact, name="contact"),
    path(
    "projects/create/",
    views.project_create,
    name="project_create"
    ),

    path(
    "projects/<int:pk>/edit/",
    views.project_update,
    name="project_update"
    ),

    path(
    "projects/<int:pk>/delete/",
    views.project_delete,
    name="project_delete"
    ),
    path(
    "projects/",
    views.ProjectListView.as_view(),
    name="project_list"
),

    path(
    "projects/<int:pk>/",
    views.ProjectDetailView.as_view(),
    name="project_detail"
),
    path(
    "tasks/create/",
    views.TaskCreateView.as_view(),
    name="task_create"
),

    path(
    "tasks/<int:pk>/edit/",
    views.TaskUpdateView.as_view(),
    name="task_update"
),

    path(
    "tasks/<int:pk>/delete/",
    views.TaskDeleteView.as_view(),
    name="task_delete"
),

]
