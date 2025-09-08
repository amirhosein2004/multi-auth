from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return f"{self.username} - {self.phone}"
