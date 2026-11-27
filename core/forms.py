from django import forms
from .models import Project, Task
from django.core.exceptions import ValidationError
from django.utils import timezone


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "project",
            "due_date",
            "status",
            "priority"
        ]

    def clean_title(self):
        title = self.cleaned_data["title"]

        if len(title.strip()) < 3:
            raise ValidationError(
                "Le titre doit contenir au moins 3 caractères."
            )

        return title

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get("due_date")

        if due_date and due_date < timezone.localdate():
            self.add_error(
                "due_date",
                "La date limite ne peut pas être dans le passé."
            )

        return cleaned_data

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "organization",
            "description",
            "is_archived"
        ]

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Nom"
    )

    email = forms.EmailField(
        label="Adresse e-mail"
    )

    message = forms.CharField(
        widget=forms.Textarea,
        label="Message"
    )
