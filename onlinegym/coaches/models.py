from django.db import models
from accounts.models import User


class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coach_profile')
    specialty = models.CharField(max_length=100)
    certifications = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.specialty} - Coach"


class CoachPosts(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    image = models.ImageField(upload_to='posts/', null=True, blank=True, verbose_name="Post Image")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title