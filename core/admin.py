from django.contrib import admin
from .models import Organization, Project, Task


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "slug")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("description", "organization", "is_archived")
    list_filter = ("is_archived", "organization")
    search_fields = ("description",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "due_date",
        "status",
        "priority",
        "created_at",
    )

    list_filter = ("status", "due_date")
    search_fields = ("title", "project__description")
    ordering = ("due_date",)
