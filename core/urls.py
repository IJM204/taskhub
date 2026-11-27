from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, api_views

app_name = "core"

urlpatterns = [
    path("api/status/", api_views.api_status, name="api_status"),
    path("", views.home, name="home"),
    path("organizations/", views.organization_list, name="organization_list"),
    path(
        "organizations/<slug:slug>/",
        views.organization_detail,
        name="organization_detail",
    ),
    path("tasks/", views.TaskListView.as_view(), name="task_list"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
    path("contact/", views.contact, name="contact"),
    path("projects/", views.ProjectListView.as_view(), name="project_list"),
    path("projects/create/", views.project_create, name="project_create"),
    path(
        "projects/<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"
    ),
    path("projects/<int:pk>/edit/", views.project_update, name="project_update"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project_delete"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="core/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path(
        "organizations/<int:organization_id>/projects/create/",
        views.project_create,
        name="project_create",
    ),
    path("projects/<int:pk>/edit/", views.project_update, name="project_update"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project_delete"),
    path(
        "api/organizations/",
        api_views.organization_api_list,
        name="api_organization_list",
    ),
    path(
        "api/tasks/",
        api_views.TaskListCreateAPIView.as_view(),
        name="api_task_list_create",
    ),
    path(
        "api/tasks/<int:pk>/",
        api_views.TaskDetailAPIView.as_view(),
        name="api_task_detail",
    ),
]
