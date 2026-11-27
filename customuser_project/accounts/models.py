from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(blank=True, verbose_name="Biographie")
    birth_date = models.DateField(
        null=True, blank=True, verbose_name="Date de naissance"
    )

    def __str__(self):
        return f"Profil de {self.user.username}"
