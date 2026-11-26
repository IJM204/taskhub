from django import forms
from .models import Project


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
