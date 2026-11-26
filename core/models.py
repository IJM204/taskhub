from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Organization(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Nom de l'organisation"
    )

    slug = models.SlugField(
        verbose_name="Identifiant URL"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"

class Project(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    description = models.TextField()

    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

class Task(models.Model):

    class Status(models.TextChoices):
        TODO = "TODO", "À faire"
        IN_PROGRESS = "IN_PROGRESS", "En cours"
        DONE = "DONE", "Terminé"

    title = models.CharField(max_length=200)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    due_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"
        ordering = ["due_date"]
    priority = models.IntegerField(
    default=3,
    validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ],
    verbose_name="Priorité"
)
