from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Organization, Task
from .serializers import OrganizationSerializer, TaskSerializer


@api_view(["GET"])
def api_status(request):
    return Response({"status": "ok"})


@api_view(["GET"])
def organization_api_list(request):
    organizations = Organization.objects.prefetch_related(
        "projects",
        "projects__tasks",
    ).all()

    serializer = OrganizationSerializer(organizations, many=True)

    return Response(serializer.data)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.select_related(
        "project",
        "project__organization",
    ).all()

    serializer_class = TaskSerializer

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = self.get_object()

        if task.status == Task.Status.DONE:
            return Response(
                {"detail": "Cette tâche est déjà terminée."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task.status = Task.Status.DONE
        task.save(update_fields=["status"])

        serializer = self.get_serializer(task)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskListCreateAPIView(ListCreateAPIView):
    queryset = Task.objects.select_related("project", "project__organization").all()
    serializer_class = TaskSerializer


class TaskDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.select_related("project", "project__organization").all()
    serializer_class = TaskSerializer
