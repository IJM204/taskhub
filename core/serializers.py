from rest_framework import serializers

from .models import Organization, Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "organization",
            "description",
            "is_archived",
        ]
        read_only_fields = ["id"]


class OrganizationSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    open_tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "slug",
            "created_at",
            "projects",
            "open_tasks_count",
        ]
        read_only_fields = fields

    def get_open_tasks_count(self, obj):
        return sum(
            1
            for project in obj.projects.all()
            for task in project.tasks.all()
            if task.status != Task.Status.DONE
        )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "project",
            "due_date",
            "created_at",
            "status",
            "priority",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_title(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Le titre doit contenir au moins 3 caractères."
            )

        return value

    def validate_priority(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                "La priorité doit être comprise entre 1 et 5."
            )

        return value

    def validate(self, attrs):
        due_date = attrs.get(
            "due_date",
            getattr(self.instance, "due_date", None),
        )

        from django.utils import timezone

        if due_date and due_date < timezone.now().date():
            raise serializers.ValidationError(
                {"due_date": "La date limite ne peut pas être dans le passé."}
            )

        return attrs
