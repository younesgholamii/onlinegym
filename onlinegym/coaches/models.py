from django.db import models
from accounts.models import User, RegularUser
from django.urls import reverse



class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coach_profile')
    specialty = models.CharField(max_length=100)
    certifications = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.specialty} - Coach"


class CoachPosts(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='posts')
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
    
    def get_absolute_url(self):
        return reverse('accounts:user_profile', args=[int(self.coach.user.id)])
    
class Appointment(models.Model):
    plan_choices = [
        ('Diet', 'Diet plan'),
        ('Exercise', 'Exercise plan')
    ]

    user = models.ForeignKey(RegularUser, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    workoutplan = models.OneToOneField("WorkoutPlan", on_delete=models.CASCADE, related_name='workout_plan', null=True, blank=True)
    answered = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11)
    age = models.SmallIntegerField()
    weight = models.SmallIntegerField()
    height = models.SmallIntegerField()
    plan = models.CharField(max_length=50, choices=plan_choices, default='D')
    descriptions = models.TextField(default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.user.username} -- {self.coach.user.username}"
    

class Exercises(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='coachs')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, null=True, blank=True)
    sets = models.SmallIntegerField()
    reps = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    user = models.ForeignKey(RegularUser, on_delete=models.CASCADE, related_name='user_workout_plan')
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class AppointmentAnswer(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='plan')
    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE, related_name='exercise')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.workout_plan} -- {self.exercise.name}'

