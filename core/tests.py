from datetime import date

from django.test import TestCase

from core.models import Organization, Project, Task

from django.contrib.auth import get_user_model
from django.urls import reverse

from datetime import timedelta
from django.utils import timezone
from core.forms import ContactForm, ProjectForm, TaskForm

from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class ViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="TestPassword123"
        )

        self.organization = Organization.objects.create(
            name="Organisation Test", slug="organisation-test"
        )

        self.project = Project.objects.create(
            organization=self.organization, description="Projet de test"
        )

    def test_home_returns_200(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)

    def test_organization_list_redirects_anonymous_user(self):
        response = self.client.get(reverse("core:organization_list"))
        self.assertEqual(response.status_code, 302)

    def test_project_update_returns_403_for_non_admin(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("core:project_update", kwargs={"pk": self.project.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_project_detail_returns_404(self):
        response = self.client.get(
            reverse("core:project_detail", kwargs={"pk": 999999})
        )
        self.assertEqual(response.status_code, 404)


class OrganizationModelTest(TestCase):
    def test_str(self):
        organization = Organization.objects.create(
            name="Tech Burundi", slug="tech-burundi"
        )
        self.assertEqual(str(organization), "Tech Burundi")

    def test_slug_generation(self):
        organization = Organization(name="Digital Burundi")
        organization.save()

        self.assertEqual(organization.slug, "digital-burundi")


class ProjectModelTest(TestCase):
    def test_str(self):
        organization = Organization.objects.create(
            name="Tech Burundi", slug="tech-burundi"
        )
        project = Project.objects.create(
            organization=organization, description="Application de gestion"
        )

        self.assertEqual(str(project), "Application de gestion")


class TaskModelTest(TestCase):
    def setUp(self):
        organization = Organization.objects.create(
            name="Tech Burundi", slug="tech-burundi"
        )
        project = Project.objects.create(
            organization=organization, description="Projet de test"
        )

        self.task = Task.objects.create(
            title="Tester Django", project=project, due_date=date(2026, 12, 31)
        )

    def test_str(self):
        self.assertEqual(str(self.task), "Tester Django")

    def test_default_status(self):
        self.assertEqual(self.task.status, Task.Status.TODO)

    def test_default_priority(self):
        self.assertEqual(self.task.priority, 3)


class FormTest(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name="Organisation Form", slug="organisation-form"
        )

        self.project = Project.objects.create(
            organization=self.organization, description="Projet formulaire"
        )

    def test_contact_form_valid(self):
        form = ContactForm(
            data={
                "name": "Medard",
                "email": "medard@example.com",
                "message": "Bonjour Django",
            }
        )
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid_email(self):
        form = ContactForm(
            data={"name": "Medard", "email": "email-invalide", "message": "Bonjour"}
        )
        self.assertFalse(form.is_valid())

    def test_project_form_valid(self):
        form = ProjectForm(
            data={
                "organization": self.organization.pk,
                "description": "Nouveau projet",
                "is_archived": False,
            }
        )
        self.assertTrue(form.is_valid())

    def test_task_form_valid(self):
        form = TaskForm(
            data={
                "title": "Développer une API",
                "project": self.project.pk,
                "due_date": (timezone.localdate() + timedelta(days=5)).isoformat(),
                "status": "TODO",
                "priority": 3,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_task_form_invalid_title(self):
        form = TaskForm(
            data={
                "title": "AB",
                "project": self.project.pk,
                "due_date": (timezone.localdate() + timedelta(days=5)).isoformat(),
                "status": "TODO",
                "priority": 3,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_task_form_past_due_date(self):
        form = TaskForm(
            data={
                "title": "Développer une API",
                "project": self.project.pk,
                "due_date": (timezone.localdate() - timedelta(days=1)).isoformat(),
                "status": "TODO",
                "priority": 3,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("due_date", form.errors)


class TaskAPITest(APITestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name="Organisation API",
            slug="organisation-api",
        )

        self.project = Project.objects.create(
            organization=self.organization,
            description="Projet API",
        )

        self.task = Task.objects.create(
            title="Tâche de test API",
            project=self.project,
            due_date=timezone.localdate() + timedelta(days=5),
        )

        self.list_url = reverse("task-list")
        self.detail_url = reverse(
            "task-detail",
            kwargs={"pk": self.task.pk},
        )

    def test_list_tasks(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        data = {
            "title": "Nouvelle tâche API",
            "project": self.project.pk,
            "due_date": (timezone.localdate() + timedelta(days=10)).isoformat(),
            "status": "TODO",
            "priority": 3,
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Nouvelle tâche API")

    def test_update_task(self):
        data = {"title": "Tâche modifiée"}

        response = self.client.patch(
            self.detail_url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Tâche modifiée")

    def test_delete_task(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_not_found(self):
        url = reverse("task-detail", kwargs={"pk": 999999})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_task_with_invalid_title(self):
        data = {
            "title": "AB",
            "project": self.project.pk,
            "due_date": (timezone.localdate() + timedelta(days=10)).isoformat(),
            "status": "TODO",
            "priority": 3,
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
