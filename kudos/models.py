from django.contrib.auth.models import AbstractUser
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    remaining_kudos = models.IntegerField(default=3)

class Kudos(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_kudos")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_kudos")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "receiver", "created_at"],
                name="unique_kudo_per_week",
            )
        ]

    def __str__(self):
        return f"Kudos from {self.sender} to {self.receiver}"
