import factory
from factory.django import DjangoModelFactory
from django.utils.text import slugify

from core.models import Organization, Project, Task


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker("company")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    organization = factory.SubFactory(OrganizationFactory)
    description = factory.Faker("sentence")


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Faker("sentence", nb_words=4)
    project = factory.SubFactory(ProjectFactory)
    due_date = factory.Faker("future_date", end_date="+30d")
    status = Task.Status.TODO
    priority = 3
