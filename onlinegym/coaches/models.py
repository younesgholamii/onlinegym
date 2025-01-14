from django.db import models
from accounts.models import User


class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coach_profile')
    specialty = models.CharField(max_length=100)
    certifications = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.specialty} - Coach"
