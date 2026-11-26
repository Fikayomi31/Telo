from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    class Role(models.TextChoices):
        TAILOR = "TAILOR", "Tailor"
        ADMIN = "ADMIN", "Administator"

    role = models.CharField(max_length=20, choices=Role, default=Role.TAILOR)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} - {self.role}"

