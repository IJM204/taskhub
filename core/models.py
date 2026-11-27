from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.conf import settings


class Membership(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrateur"
        MEMBER = "MEMBER", "Membre"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships"
    )
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "organization"], name="unique_user_organization"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.organization} ({self.role})"


class Organization(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nom de l'organisation")

    slug = models.SlugField(unique=True, verbose_name="Identifiant URL")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"


class Project(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="projects"
    )

    description = models.TextField()

    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"


class TaskQuerySet(models.QuerySet):
    def open(self):
        return self.exclude(status=Task.Status.DONE)

    def overdue(self):
        from django.utils import timezone

        return self.filter(due_date__lt=timezone.now().date()).exclude(
            status=Task.Status.DONE
        )


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "TODO", "À faire"
        IN_PROGRESS = "IN_PROGRESS", "En cours"
        DONE = "DONE", "Terminé"

    title = models.CharField(max_length=200)
    title_normalized = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Titre normalisé",
    )
    assigned_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Assignment",
        related_name="assigned_tasks",
        blank=True,
    )

    objects = TaskQuerySet.as_manager()

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")

    due_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.TODO
    )

    priority = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Priorité",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"
        ordering = ["due_date"]
        indexes = [
            models.Index(fields=["due_date"], name="task_due_date_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(priority__gte=1, priority__lte=5),
                name="task_priority_1_5",
            ),
        ]


class Assignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="assignments")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_assignments",
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task", "user"], name="unique_task_user_assignment"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.task}"
