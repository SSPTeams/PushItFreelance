from django.contrib.auth.models import AbstractUser
from django.db import models


class Freelancer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
