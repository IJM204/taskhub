from django import forms


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
